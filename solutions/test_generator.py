#!/usr/bin/env python3
"""
ai_test_generator.py

Reads cses_problems.json, scrapes each problem statement,
and uses Perplexity Sonar Pro to generate 10 small + 10 large test cases,
saving results under cses_tests/.
"""

import os
import sys
import json
import time
import shutil
import requests
import argparse
import traceback
from bs4 import BeautifulSoup

API_URL = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar-pro"
PROBLEMS = "cses_problems.json"
OUTPUT = "cses_tests"

HEADERS_TMPL = {
    "Authorization": None,
    "Content-Type": "application/json"
}

PROMPT_TMPL = """
You are an expert competitive programmer and test-generator. Given the following CSES problem, produce {small} small and {large} large test cases. For each, provide input and expected output. But do it in a way that it can be evaluated in python.

Problem Title:
{title}

Problem Description:
{description}

Input Format:
{input_format}

Output Format:
{output_format}

Constraints:
{constraints}

Return only a JSON array of objects:
[
  {{ "size":"small", "input":"…", "output":"…" }},
  …,
  {{ "size":"large", "input":"…", "output":"…" }}
]
"""


def load_problems():
    with open(PROBLEMS, encoding="utf-8") as f:
        return json.load(f)


def scrape_statement(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    c = soup.find("div", class_="content")

    title = c.find("h1").get_text(strip=True)
    desc = "\n".join(p.get_text(strip=True) for p in c.find_all("p", recursive=False))

    inp = ""
    outp = ""
    cons = ""

    for h in c.find_all(["h2", "h3"]):
        text = h.get_text(strip=True).lower()
        nxt = h.find_next_sibling()
        if not nxt:
            continue
        block = nxt.get_text(strip=True)
        if text == "input":
            inp = block
        elif text == "output":
            outp = block
        elif "constraint" in text:
            cons = block

    return title, desc, inp, outp, cons


def generate_ai_tests(problem, api_key, small=10, large=10):
    title, desc, inp, outp, cons = scrape_statement(problem["url"])
    prompt = PROMPT_TMPL.format(
        small=small,
        large=large,
        title=title,
        description=desc,
        input_format=inp,
        output_format=outp,
        constraints=cons
    )

    headers = HEADERS_TMPL.copy()
    headers["Authorization"] = f"Bearer {api_key}"

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You generate test cases for CSES problems."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.2
    }

    try:
        r = requests.post(API_URL, headers=headers, json=body, timeout=60)
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"].strip()

        jstart, jend = text.find("["), text.rfind("]") + 1
        text = text[jstart:jend].strip()

        print(text)  # Debug output — can be removed if not needed
        # Eval is used here carefully to parse the list from string JSON-like format
        tests_list = eval(text)

        json_string = json.dumps(tests_list)
        print(json_string)  # Debug output — can be removed if not needed

        return json.loads(json_string)

    except Exception as e:
        print(f"  ✘ Failed: {e}")
        traceback.print_exc(file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True, help="Perplexity Sonar Pro API key")
    parser.add_argument("--small", type=int, default=10, help="Number of small test cases to generate")
    parser.add_argument("--large", type=int, default=10, help="Number of large test cases to generate")
    args = parser.parse_args()

    if os.path.exists(OUTPUT):
        shutil.rmtree(OUTPUT)  # Clear the output directory
    os.makedirs(OUTPUT, exist_ok=True)

    problems = load_problems()

    for pr in problems:
        pid = pr["id"]
        name = pr["name"].replace(" ", "_")
        print(f"Generating AI tests for {pid}_{name}...")
        try:
            tests = generate_ai_tests(pr, args.api_key, args.small, args.large)
            output_data = {
                "problem_id": pid,
                "problem_name": pr["name"],
                "tests": tests
            }
            output_path = os.path.join(OUTPUT, f"{pid}_{name}_ai_tests.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)
            print("  ✔ Saved")
        except Exception as e:
            print(f"  ✘ Failed: {e}")
            traceback.print_exc(file=sys.stderr)
        time.sleep(2)  # Pause to avoid rate limits


if __name__ == "__main__":
    main()
