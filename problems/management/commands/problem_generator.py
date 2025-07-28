import os
import json
import time
import requests
from typing import Dict
from tqdm import tqdm
from bs4 import BeautifulSoup
import google.generativeai as genai
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from problems.models import Problem

class Command(BaseCommand):
    help = 'Generate and populate problems from CSES using Gemini API and web scraping'

    def __init__(self):
        super().__init__()
        self.daily_requests = 0
        self.daily_reset_time = time.time()
        self.max_daily_requests = 50  # Free tier limit for gemini-1.5-flash

    GEMINI_PROMPT = """
Given the following competitive programming problem HTML content and its URL, extract and summarize its core metadata fields.

Return a JSON object with these keys:
"title": problem title (string),
"description": clean extended description concisely summarizing what needs to be solved (string),
"input_format": only the actual input specification (not Input heading, not examples) (string),
"output_format": the output specification (string),
"constraints": all numerical and textual constraints from statement (string),
"difficulty": estimate as one of ["easy", "medium", "hard"] (string),
"time_limit": integer, in milliseconds, default 1000 if missing,
"memory_limit": integer, in MB, default 256 if missing.

Make your output valid JSON. Only give the JSON object.

PROBLEM URL: {url}

HTML STATEMENT:
===
{html}
===
"""

    def gemini_extract(self, llm, url: str, html: str) -> Dict:
        """Send prompt to Gemini, parse and validate the JSON response."""
        try:
            # Enforce daily quota
            self._enforce_rate_limit()
            prompt = self.GEMINI_PROMPT.format(url=url, html=html)
            resp = llm.generate_content(prompt)
            if not hasattr(resp, 'text') or not resp.text:
                raise ValueError("Gemini API response is empty or invalid")
            text = resp.text.strip()

            # Precisely strip markdown code fences
            if text.startswith("```"):
                parts = text.split("\n", 1)
                text = parts[1] if len(parts) > 1 else parts[0].lstrip("```").strip()
            if text.endswith("```"):
                text = text.rsplit("```", 1)[0].strip()

            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f"JSON decode error for {url}: {e}"))
                self.stdout.write(f"Raw: {text}")
                raise

            # Validate required fields
            for fld in ("title", "description", "input_format", "output_format", "constraints", "difficulty"):
                if fld not in data:
                    raise ValueError(f"Missing field: {fld}")
            if data["difficulty"] not in ("easy", "medium", "hard"):
                raise ValueError(f"Invalid difficulty: {data['difficulty']}")

            # Coerce numeric limits
            data["time_limit"] = max(1, int(data.get("time_limit", 1000)))
            data["memory_limit"] = max(1, int(data.get("memory_limit", 256)))

            self.daily_requests += 1
            return data
        except genai.types.generation_types.BlockedPromptException as e:
            self.stdout.write(self.style.ERROR(f"Gemini API blocked prompt for {url}: {e}"))
            raise
        except genai.types.generation_types.StopCandidateException as e:
            self.stdout.write(self.style.ERROR(f"Gemini API stopped generation for {url}: {e}"))
            raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected Gemini API error for {url}: {e}"))
            raise

    def scrape_problem_html(self, url: str) -> str:
        """Fetch and parse the problem statement HTML."""
        try:
            r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            div = soup.find("div", class_="content")
            if not div:
                raise ValueError("No content div found")
            # Remove unnecessary tags to reduce token usage
            for tag in div(["script", "style", "nav", "footer"]):
                tag.decompose()
            return str(div)
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"HTTP error while fetching {url}: {e}"))
            raise
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Scraping error for {url}: {e}"))
            raise

    def _enforce_rate_limit(self):
        """Enforce daily request limit (50 RPD for free tier)."""
        current_time = time.time()
        # Reset daily counter if new day
        if current_time - self.daily_reset_time > 86400:
            self.daily_requests = 0
            self.daily_reset_time = current_time
        # Check daily limit
        if self.daily_requests >= self.max_daily_requests:
            self.stdout.write(self.style.WARNING("Daily request limit reached (50 requests). Waiting for reset..."))
            time_to_reset = 86400 - (current_time - self.daily_reset_time)
            time.sleep(time_to_reset + 60)  # Wait until reset + buffer
            self.daily_requests = 0
            self.daily_reset_time = time.time()

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting CSES problem ingestion…"))

        # Load Gemini API key from settings
        api_key = getattr(settings, "GEMINI_API_KEY", None)
        if not api_key:
            self.stdout.write(self.style.ERROR("GEMINI_API_KEY missing in settings.py"))
            return
        genai.configure(api_key=api_key)
        model = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")
        llm = genai.GenerativeModel(model)

        # Get default author
        User = get_user_model()
        default_author = User.objects.filter(is_superuser=True).first()
        if not default_author:
            self.stdout.write(self.style.ERROR("No superuser found. Please create a user with 'python manage.py createsuperuser'."))
            return

        # Load problem list JSON
        path = os.path.join(settings.BASE_DIR, "solutions", "cses_problems.json")
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f"File not found: {path}"))
            return
        try:
            with open(path, encoding="utf-8") as f:
                problems = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Failed to parse {path}: {e}"))
            return
        except IOError as e:
            self.stdout.write(self.style.ERROR(f"Failed to read {path}: {e}"))
            return

        self.stdout.write(f"Loaded {len(problems)} problems")

        with transaction.atomic():
            Problem.objects.all().delete()  # Flush existing problems

            for item in tqdm(problems, desc="Processing", unit="prob"):
                pid = item.get("id")
                url = item.get("url")
                if not pid or not url:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid entry: {item}"))
                    continue

                try:
                    html = self.scrape_problem_html(url)
                    try:
                        data = self.gemini_extract(llm, url, html)
                    except Exception:
                        # Fallback to paid model if free-tier fails
                        if model.endswith("-free"):
                            llm = genai.GenerativeModel("gemini-1.5-flash")
                            data = self.gemini_extract(llm, url, html)
                        else:
                            raise

                    Problem.objects.create(
                        id=pid,
                        url=url,
                        title=data["title"],
                        description=data["description"],
                        input_format=data["input_format"],
                        output_format=data["output_format"],
                        constraints=data["constraints"],
                        difficulty=data["difficulty"],
                        time_limit=data["time_limit"],
                        memory_limit=data["memory_limit"],
                        author=default_author
                    )
                    self.stdout.write(self.style.SUCCESS(f"Added problem {pid}"))

                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"DB error for {pid}: {e}"))
                    continue
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed {pid}: {e}"))
                    continue

                # Delay to respect rate limits
                delay = getattr(settings, "CSES_SCRAPE_DELAY", 1.0)
                time.sleep(delay)

        self.stdout.write(self.style.SUCCESS("All problems ingested successfully"))
