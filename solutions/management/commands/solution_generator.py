from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from problems.models import Problem

import os
import sys
import json
import time
import shutil
import traceback
import subprocess
import google.generativeai as genai
from typing import List, Dict, Set
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class CSESSolutionGenerator:
    def __init__(self, stdout, stderr, chromedriver_path: str = "/usr/local/bin/chromedriver"):
        self.stdout = stdout
        self.stderr = stderr
        self.api_key = getattr(settings, "GEMINI_API_KEY", None)
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY missing in settings.py")
        self.chromedriver_path = chromedriver_path
        self.sample_tests_dir = os.path.join(settings.BASE_DIR, "solutions", "cses_sample_tests")
        self.solutions_dir = os.path.join(settings.BASE_DIR, "solutions", "cses_solutions")
        self.base_url = "https://cses.fi"
        self.problemset_url = "https://cses.fi/problemset/"
        self.problems_data = []
        self.daily_requests = 0
        self.daily_reset_time = time.time()
        self.max_daily_requests = 50  # Free tier limit for gemini-pro

        os.makedirs(self.solutions_dir, exist_ok=True)
        os.makedirs(self.sample_tests_dir, exist_ok=True)

    def _enforce_rate_limit(self):
        """Enforce Gemini API daily request limit (50 RPD for free tier)."""
        current_time = time.time()
        if current_time - self.daily_reset_time > 86400:
            self.daily_requests = 0
            self.daily_reset_time = current_time
        if self.daily_requests >= self.max_daily_requests:
            self.stdout.write(f"Daily request limit reached ({self.max_daily_requests} requests). Waiting for reset...")
            time_to_reset = 86400 - (current_time - self.daily_reset_time)
            time.sleep(time_to_reset + 60)
            self.daily_requests = 0
            self.daily_reset_time = time.time()

    def setup_driver(self, headless: bool = True) -> webdriver.Chrome:
        try:
            options = Options()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            service = ChromeService(executable_path=self.chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e:
            self.stderr.write(f"Error setting up ChromeDriver: {e}")
            traceback.print_exc()
            return None

    def scrape_problemset(self) -> List[Dict]:
        driver = self.setup_driver()
        if not driver:
            return []
        try:
            self.stdout.write("Scraping CSES problemset...")
            driver.get(self.problemset_url)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "task-list"))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            problems = []
            task_tables = soup.find_all('ul', class_='task-list')[1:]
            for table in task_tables:
                heading = table.find_previous('h2')
                category = heading.text.strip() if heading else "Unknown"
                rows = table.find_all('li')
                for row in rows:
                    link = row.find('a')
                    if not link:
                        continue
                    problem_id = link['href'].split('/')[-1]
                    problem_name = link.text.strip()
                    solved_span = row.find('span', class_='detail')
                    solved_count = solved_span.text.strip() if solved_span else "0"
                    problems.append({
                        'category': category,
                        'id': problem_id,
                        'name': problem_name,
                        'solved_count': solved_count,
                        'url': f"{self.base_url}{link['href']}"
                    })
            self.stdout.write(f"Scraped {len(problems)} problems from CSES")
            self.problems_data = problems
            return problems
        except Exception as e:
            self.stderr.write(f"Error scraping problemset: {e}")
            traceback.print_exc()
            return []
        finally:
            if driver:
                driver.quit()

    def save_problems_data(self):
        """Save scraped problems data to JSON."""
        try:
            filepath = os.path.join(settings.BASE_DIR, "solutions", "cses_problems.json")
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.problems_data, f, indent=2, ensure_ascii=False)
            self.stdout.write(f"Saved problems data to {filepath}")
        except Exception as e:
            self.stderr.write(f"Error saving problems data: {e}")

    def extract_sample_test_cases(self, content_div) -> List[Dict[str, str]]:
        test_cases = []
        try:
            sample_sections = content_div.find_all(['h2', 'h3'])
            current_input = ""
            current_output = ""
            for heading in sample_sections:
                heading_text = heading.get_text().strip().lower()
                if 'sample input' in heading_text or 'example input' in heading_text:
                    next_elem = heading.find_next_sibling()
                    while next_elem and next_elem.name not in ['pre', 'code', 'h2', 'h3']:
                        next_elem = next_elem.find_next_sibling()
                    if next_elem and next_elem.name in ['pre', 'code']:
                        current_input = next_elem.get_text().strip()
                    elif next_elem and next_elem.name not in ['h2', 'h3']:
                        current_input = next_elem.get_text().strip()
                elif 'sample output' in heading_text or 'example output' in heading_text:
                    next_elem = heading.find_next_sibling()
                    while next_elem and next_elem.name not in ['pre', 'code', 'h2', 'h3']:
                        next_elem = next_elem.find_next_sibling()
                    if next_elem and next_elem.name in ['pre', 'code']:
                        current_output = next_elem.get_text().strip()
                    elif next_elem and next_elem.name not in ['h2', 'h3']:
                        current_output = next_elem.get_text().strip()
                    if current_input and current_output:
                        test_cases.append({
                            'input': current_input,
                            'output': current_output
                        })
                        current_input = ""
                        current_output = ""
            if not test_cases:
                pre_blocks = content_div.find_all(['pre', 'code'])
                for i in range(0, len(pre_blocks) - 1, 2):
                    if i + 1 < len(pre_blocks):
                        input_text = pre_blocks[i].get_text().strip()
                        output_text = pre_blocks[i + 1].get_text().strip()
                        if input_text and output_text:
                            test_cases.append({
                                'input': input_text,
                                'output': output_text
                            })
        except Exception as e:
            self.stderr.write(f"Error extracting sample test cases: {e}")
        return test_cases

    def save_sample_test_cases(self, problem_id: str, problem_name: str, test_cases: List[Dict[str, str]]):
        try:
            if not test_cases:
                self.stdout.write(f"No sample test cases found for {problem_name}")
                return
            clean_name = "".join(c for c in problem_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_name = clean_name.replace(' ', '_')
            filename = f"{problem_id}_{clean_name}_samples.json"
            filepath = os.path.join(self.sample_tests_dir, filename)
            sample_data = {
                'problem_id': problem_id,
                'problem_name': problem_name,
                'sample_count': len(test_cases),
                'test_cases': test_cases,
                'scraped_at': datetime.now().isoformat()
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
            self.stdout.write(f"Saved {len(test_cases)} sample test cases to {filepath}")
        except Exception as e:
            self.stderr.write(f"Error saving sample test cases: {e}")

    def scrape_problem_statement(self, problem_url: str) -> Dict[str, str]:
        driver = self.setup_driver()
        if not driver:
            return {}
        try:
            driver.get(problem_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "content"))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            content_div = soup.find('div', class_='content')
            if not content_div:
                return {}
            title = content_div.find('h1')
            title_text = title.text.strip() if title else "Unknown Problem"
            description_parts = []
            for elem in content_div.find_all(['p', 'ul', 'li']):
                if elem.name == 'p':
                    description_parts.append(elem.get_text().strip())
                elif elem.name == 'ul':
                    for li in elem.find_all('li'):
                        description_parts.append(f"- {li.get_text().strip()}")
            description = '\n'.join(description_parts)
            input_section, output_section, constraints_section = "", "", ""
            headings = content_div.find_all(['h2', 'h3'])
            for heading in headings:
                heading_text = heading.get_text().strip().lower()
                next_elem = heading.find_next_sibling()
                if 'input' in heading_text:
                    if next_elem:
                        input_section = next_elem.get_text().strip()
                elif 'output' in heading_text:
                    if next_elem:
                        output_section = next_elem.get_text().strip()
                elif 'constraint' in heading_text:
                    if next_elem:
                        constraints_section = next_elem.get_text().strip()
            sample_test_cases = self.extract_sample_test_cases(content_div)
            return {
                'title': title_text,
                'description': description,
                'input_format': input_section,
                'output_format': output_section,
                'constraints': constraints_section,
                'sample_test_cases': sample_test_cases
            }
        except Exception as e:
            self.stderr.write(f"Error scraping problem statement: {e}")
            return {}
        finally:
            if driver:
                driver.quit()

    def generate_solution_with_gemini(self, problem_data: Dict[str, str]) -> str:
        try:
            self._enforce_rate_limit()
            prompt = f"""You are an expert competitive programmer. Given the following CSES problem, write a complete, correct, and efficient Python 3 solution.

Problem Title: {problem_data.get('title', 'Unknown')}

Problem Description:
{problem_data.get('description', '')}

Input Format:
{problem_data.get('input_format', '')}

Output Format:
{problem_data.get('output_format', '')}

Constraints:
{problem_data.get('constraints', '')}

Requirements:
1. Write complete Python 3 code that reads from standard input and writes to standard output
2. Use efficient algorithms suitable for competitive programming
3. Handle edge cases appropriately
4. Include minimal comments explaining the approach
5. Use PyPy3 compatible code (avoid deep recursion if possible)
6. Optimize for time complexity

Provide only the Python code solution wrapped in python code blocks:
```python
# Your solution here
```
"""
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            response = model.generate_content(
                prompt, generation_config={"temperature": 0.2, "max_output_tokens": 2048}
            )
            solution = response.text.strip()
            
            # Enhanced code extraction logic
            code = self._extract_code_from_response(solution)
            if not code:
                self.stderr.write("Error: Could not extract valid Python code from Gemini response")
                self.stderr.write(f"Raw response: {solution[:500]}...")  # Show first 500 chars for debugging
                return ""
                
            self.daily_requests += 1
            return code
        except Exception as e:
            self.stderr.write(f"Unexpected error generating solution with Gemini: {e}")
            return ""

    def _extract_code_from_response(self, response_text: str) -> str:
        """Enhanced code extraction with multiple fallback methods."""
        response_text = response_text.strip()
        
        # Method 1: Look for ```python code blocks
        python_start = response_text.find("```python")
        if python_start != -1:
            code_start = python_start + len("```python")
            # Skip any newlines after ```python
            while code_start < len(response_text) and response_text[code_start] in ['\n', '\r']:
                code_start += 1
            code_end = response_text.find("```", code_start)
            if code_end != -1:
                code = response_text[code_start:code_end].strip()
                if code:
                    return code
        
        # Method 2: Look for any ``` code blocks
        code_start = response_text.find("```")
        if code_start != -1:
            # Skip the opening ```
            code_start += 3
            # Skip language identifier if present (like "python")
            first_newline = response_text.find('\n', code_start)
            if first_newline != -1:
                code_start = first_newline + 1
            code_end = response_text.find("```", code_start)
            if code_end != -1:
                code = response_text[code_start:code_end].strip()
                if code and ('input()' in code or 'print(' in code or 'import' in code):
                    return code
        
        # Method 3: Look for Python-like patterns without code blocks
        lines = response_text.split('\n')
        python_lines = []
        in_code_section = False
        
        for line in lines:
            stripped = line.strip()
            # Start collecting if we see typical Python patterns
            if any(pattern in stripped for pattern in ['import ', 'def ', 'if __name__', 'input()', 'print(']):
                in_code_section = True
            
            if in_code_section:
                # Stop if we hit explanatory text
                if stripped and not any(c in stripped for c in ['#', 'import', 'def', 'class', 'if', 'for', 'while', 'try', 'except', 'input(', 'print(', '=', '+', '-', '*', '/', '<', '>', 'and', 'or', 'not', 'in', 'return']):
                    if len(stripped) > 50 and not stripped.startswith('"""'):  # Likely explanation text
                        break
                python_lines.append(line)
        
        if python_lines:
            code = '\n'.join(python_lines).strip()
            # Basic validation - should have input/output operations
            if any(pattern in code for pattern in ['input()', 'print(', 'sys.stdin', 'sys.stdout']):
                return code
        
        # Method 4: Return the entire response if it looks like code
        if any(pattern in response_text for pattern in ['input()', 'print(', 'import ', 'def main']):
            return response_text
        
        return ""

    def save_solution(self, problem_id: str, problem_name: str, solution_code: str) -> str:
        try:
            clean_name = "".join(c for c in problem_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_name = clean_name.replace(' ', '_')
            filename = f"{problem_id}_{clean_name}.py"
            filepath = os.path.join(self.solutions_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# CSES Problem: {problem_name}\n")
                f.write(f"# Problem ID: {problem_id}\n")
                f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(solution_code)
            return filepath
        except Exception as e:
            self.stderr.write(f"Error saving solution: {e}")
            return ""

    def test_solution(self, solution_file: str, test_input: str = None) -> bool:
        if not test_input:
            return True
        try:
            result = subprocess.run(
                [sys.executable, solution_file],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            self.stderr.write(f"Error testing solution: {e}")
            return False

    def generate_solutions_for_ids(self, problem_ids: Set[str], max_problems: int = None) -> int:
        if not self.problems_data:
            self.stderr.write("No problems data available. Run scrape_problemset() first.")
            return 0
        
        filtered_problems = [p for p in self.problems_data if p['id'] in problem_ids]
        if max_problems is not None:
            filtered_problems = filtered_problems[:max_problems]
        
        self.stdout.write(f"Generating solutions for {len(filtered_problems)} problems matching your provided IDs.")
        generated_count = 0
        
        for i, problem in enumerate(filtered_problems):
            try:
                self.stdout.write(f"\n[{i+1}/{len(filtered_problems)}] Processing: {problem['name']}")
                problem_statement = self.scrape_problem_statement(problem['url'])
                
                if problem_statement.get('sample_test_cases'):
                    self.save_sample_test_cases(
                        problem['id'],
                        problem['name'],
                        problem_statement['sample_test_cases']
                    )
                
                if not problem_statement:
                    self.stderr.write(f"Failed to scrape problem statement for {problem['name']}")
                    continue
                
                solution = self.generate_solution_with_gemini(problem_statement)
                if not solution:
                    self.stderr.write(f"Failed to generate solution for {problem['name']}")
                    continue
                
                filepath = self.save_solution(problem['id'], problem['name'], solution)
                if filepath:
                    self.stdout.write(f"✅ Solution saved: {filepath}")
                    generated_count += 1
                    
                    # Update Problem model with solution_code
                    try:
                        problem_obj = Problem.objects.get(id=problem['id'])
                        problem_obj.solution_code = solution
                        problem_obj.save()
                    except Problem.DoesNotExist:
                        self.stderr.write(f"Problem {problem['id']} not found in database")
                    except IntegrityError as e:
                        self.stderr.write(f"DB error updating solution for {problem['id']}: {e}")
                else:
                    self.stderr.write(f"Failed to save solution for {problem['name']}")
                
                time.sleep(2)
            except Exception as e:
                self.stderr.write(f"Error processing problem {problem['name']}: {e}")
                continue
        
        self.stdout.write(f"\n🎉 Generated {generated_count} solutions for provided problem IDs")
        return generated_count


class Command(BaseCommand):
    help = "Generate CSES problem solutions using Gemini API for problems listed in the DB."

    def add_arguments(self, parser):
        parser.add_argument(
            '--chromedriver', type=str, default='/usr/local/bin/chromedriver',
            help='Path to ChromeDriver executable'
        )
        parser.add_argument(
            '--max-problems', type=int,
            help='Maximum number of problems to generate solutions for'
        )
        parser.add_argument(
            '--scrape-only', action='store_true',
            help='Only scrape problem metadata, do not generate solutions'
        )

    def handle(self, *args, **options):
        chromedriver = options['chromedriver']
        max_problems = options.get('max_problems')
        scrape_only = options.get('scrape_only')

        generator = CSESSolutionGenerator(self.stdout, self.stderr, chromedriver)
        
        # Fetch problem IDs from the DB
        User = get_user_model()
        default_author = User.objects.filter(is_superuser=True).first()
        if not default_author:
            self.stderr.write("No superuser found. Please create a user with 'python manage.py createsuperuser'.")
            return

        problem_qs = Problem.objects.values_list('id', flat=True).distinct()
        problem_ids = set(str(pid) for pid in problem_qs)

        if not problem_ids:
            self.stderr.write("No problems found in DB. Exiting.")
            return

        self.stdout.write(f"Found {len(problem_ids)} unique problems in the database.")
        
        # Scrape problemset metadata
        scraped_problems = generator.scrape_problemset()
        if not scraped_problems:
            self.stderr.write("Failed to scrape problem metadata. Exiting.")
            return
        
        # Save scraped data
        generator.save_problems_data()

        if scrape_only:
            self.stdout.write("Scraping completed. Exiting as per --scrape-only flag.")
            return
        
        # Clear folders before generating
        for folder in [generator.solutions_dir, generator.sample_tests_dir]:
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)
        
        # Generate solutions for problems matching DB IDs
        generator.generate_solutions_for_ids(problem_ids, max_problems)