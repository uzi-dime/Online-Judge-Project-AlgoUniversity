#!/usr/bin/env python3
"""
test_generator.py

Reads cses_problems.json, scrapes each problem statement,
loads existing sample tests, embeds solution code into prompt,
uses Gemini API to generate test cases,
validates each test case by running solution script,
and saves only validated test cases under cses_tests/.

Fixes error of passing code content as path to subprocess.
"""

import os
import sys
import json
import time
import shutil
import re
import glob
import traceback
import subprocess
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')
import django
django.setup()
from django.conf import settings

# Constants and Paths
BASE_DIR = settings.BASE_DIR
MODEL = "gemini-2.5-flash-lite"
PROBLEMS = "cses_problems.json"
OUTPUT = "cses_tests"
SAMPLE_TESTS_DIR = os.path.join(BASE_DIR, "solutions", "cses_sample_tests")
SOLUTIONS_DIR = os.path.join(BASE_DIR, "solutions", "cses_solutions")

PROMPT_TMPL = """
You are an expert competitive programmer and test-generator.

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

Existing sample tests (for your reference):
{sample_tests}

Here is the reference solution code for this problem:

{solution_code}

text

Use the above solution code to generate {small} small and {large} large test cases. For each test case:

- Provide the input.
- Compute the expected output exactly as the solution would produce it.
- Format all test cases EXACTLY as a JSON array of objects with keys "size", "input", and "output".
- Return ONLY the JSON array, no explanations or additional text.
"""


def load_problems():
    with open(PROBLEMS, encoding="utf-8") as f:
        return json.load(f)


def scrape_statement(url: str):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    content_div = soup.find("div", class_="content")

    title = content_div.find("h1").get_text(strip=True)
    desc = "\n".join(p.get_text(strip=True) for p in content_div.find_all("p", recursive=False))

    inp = ""
    outp = ""
    cons = ""

    for h in content_div.find_all(["h2", "h3"]):
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


def find_sample_test_file(problem_id_prefix: str):
    pattern = os.path.join(SAMPLE_TESTS_DIR, f"{problem_id_prefix}*.json")
    matching_files = glob.glob(pattern)
    if not matching_files:
        return None
    return matching_files[0]


def load_sample_tests(problem_id: str):
    prefix = problem_id.split("_")[0]
    sample_test_file = find_sample_test_file(prefix)
    if not sample_test_file:
        return None
    try:
        with open(sample_test_file, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("problem_id") and not data["problem_id"].startswith(prefix):
            print(f"Warning: sample test file {sample_test_file} problem_id mismatch")
        return data
    except Exception as e:
        print(f"Warning: Failed to load sample tests from {sample_test_file}: {e}")
        return None


def format_sample_tests_for_prompt(sample_data):
    if not sample_data or "test_cases" not in sample_data:
        return "No sample tests available."

    lines = []
    for i, testcase in enumerate(sample_data["test_cases"], 1):
        inp = testcase.get("input", "").replace('\n', '\\n')
        outp = testcase.get("output", "").replace('\n', '\\n')
        lines.append(f"Sample Test #{i}:\nInput: {inp}\nOutput: {outp}")
    return "\n\n".join(lines)


def extract_json_array(text: str):
    text = text.strip()
    while text.startswith("``````"):
        text = text[3:-3].strip()

    pattern = re.compile(r"\[\s*(\{.*?\}\s*,?\s*)+\]", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(0)

    jstart = text.find("[")
    jend = text.rfind("]") + 1
    if jstart == -1 or jend == 0 or jend <= jstart:
        raise ValueError("Failed to find JSON array in model response")

    return text[jstart:jend]


def read_solution_code(problem_id, problem_name):
    """
    Returns the content of the solution script file for embedding in prompt.
    """
    safe_name = re.sub(r"[^\w\d-]+", "_", problem_name)
    solution_path = os.path.join(SOLUTIONS_DIR, f"{problem_id}_{safe_name}.py")
    if os.path.isfile(solution_path):
        try:
            with open(solution_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not read solution code for {problem_id}: {e}")
            return None
    glob_candidates = glob.glob(os.path.join(SOLUTIONS_DIR, f"{problem_id}_*.py"))
    if glob_candidates:
        try:
            with open(glob_candidates[0], "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not read solution code for {problem_id}: {e}")
    return None


def find_solution_script_path(problem_id, problem_name):
    """
    Returns filesystem path to the solution script file to use during validation subprocess.
    """
    safe_name = re.sub(r"[^\w\d-]+", "_", problem_name)
    solution_path = os.path.join(SOLUTIONS_DIR, f"{problem_id}_{safe_name}.py")
    if os.path.isfile(solution_path):
        return solution_path
    candidates = glob.glob(os.path.join(SOLUTIONS_DIR, f"{problem_id}_*.py"))
    if candidates:
        return candidates[0]
    return None


def generate_gemini_tests(problem, llm, small=10, large=10, sample_tests_data=None, retries=2):
    title, desc, inp, outp, cons = scrape_statement(problem["url"])
    sample_tests_text = format_sample_tests_for_prompt(sample_tests_data)
    solution_code = read_solution_code(problem["id"], problem["name"])

    if not solution_code:
        print(f"⚠️ Warning: No solution code found for problem {problem['id']} - {problem['name']}")

    prompt = PROMPT_TMPL.format(
        small=small,
        large=large,
        title=title,
        description=desc,
        input_format=inp,
        output_format=outp,
        constraints=cons,
        sample_tests=sample_tests_text,
        solution_code=solution_code or "# Solution code not available"
    )

    for attempt in range(retries + 1):
        try:
            response = llm.generate_content(prompt)
            text = response.text.strip()
            json_text = extract_json_array(text)
            tests_list = json.loads(json_text)

            if not isinstance(tests_list, list):
                raise ValueError("Parsed JSON is not a list")
            for test_case in tests_list:
                if not all(k in test_case for k in ("size", "input", "output")):
                    raise ValueError(f"Malformed test case object: {test_case}")

            return tests_list

        except Exception as e:
            if attempt < retries:
                wait_time = 2 ** attempt
                print(f"  ✗ Attempt {attempt+1} failed, retrying after {wait_time}s... Error: {e}")
                time.sleep(wait_time)
            else:
                print(f"  ✘ Failed to generate tests for problem {problem['id']} after {retries + 1} attempts: {e}")
                traceback.print_exc(file=sys.stderr)

    return []


def run_solution_on_input(solution_path: str, input_str: str, timeout=5) -> str | None:
    try:
        proc = subprocess.run(
            [sys.executable, solution_path],
            input=input_str,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            cwd=os.path.dirname(solution_path) if os.path.dirname(solution_path) else None,
            text=True,
            check=False,
        )
        output = proc.stdout.strip()
        if proc.returncode != 0:
            print(f"⚠️ Solution exited with return code {proc.returncode}")
            if proc.stderr.strip():
                print(f"stderr:\n{proc.stderr.strip()}")
            return None
        if output == "":
            if proc.stderr.strip():
                print(f"⚠️ Solution stderr (no stdout):\n{proc.stderr.strip()}")
            else:
                print(f"⚠️ Solution produced empty output for input:\n{input_str}")
            return None
        return output
    except subprocess.TimeoutExpired:
        print(f"⚠️ Solution timed out on input:\n{input_str}")
    except Exception as e:
        print(f"⚠️ Error running solution on input:\n{input_str}\nError: {e}")
    return None


def validate_test_cases(solution_path: str, test_cases: list) -> list:
    if not solution_path:
        print("⚠️ No solution script found, skipping validation.")
        return test_cases

    valid_cases = []
    for idx, test_case in enumerate(test_cases, 1):
        inp = test_case["input"]
        expected_output = test_case["output"].strip()
        actual_output = run_solution_on_input(solution_path, inp)
        if actual_output is None:
            print(f"  ✗ Test case #{idx}: execution failed, discarding.")
            continue
        if actual_output == expected_output:
            valid_cases.append(test_case)
        else:
            print(f"  ✗ Test case #{idx}: output mismatch.\nExpected: {expected_output!r}\nActual:   {actual_output!r}")
    print(f"  ✔ Validation complete: {len(valid_cases)} / {len(test_cases)} test cases passed.")
    return valid_cases


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    genai.configure(api_key=api_key)
    llm = genai.GenerativeModel(MODEL)

    if os.path.exists(OUTPUT):
        shutil.rmtree(OUTPUT)
    os.makedirs(OUTPUT, exist_ok=True)

    problems = load_problems()

    for pr in problems:
        pid = pr["id"]
        pname = pr["name"]
        safe_name = re.sub(r"[^\w\d-]+", "_", pname)

        print(f"Generating Gemini AI tests for {pid}_{safe_name} ...")

        sample_tests_data = load_sample_tests(pid)
        if sample_tests_data:
            print(f"  ✔ Loaded sample tests from {sample_tests_data.get('problem_id')}")

        try:
            generated_tests = generate_gemini_tests(pr, llm, small=10, large=10, sample_tests_data=sample_tests_data)

            combined_tests = []
            if sample_tests_data and "test_cases" in sample_tests_data:
                for st in sample_tests_data["test_cases"]:
                    combined_tests.append({
                        "size": "sample",
                        "input": st["input"],
                        "output": st["output"],
                    })
            combined_tests.extend(generated_tests)

            solution_script_path = find_solution_script_path(pid, pname)
            if solution_script_path:
                print(f"  ✔ Validating all test cases against solution script at {solution_script_path} ...")
                combined_tests = validate_test_cases(solution_script_path, combined_tests)
            else:
                print("⚠️ No solution script file found. Skipping validation.")

            output_data = {
                "problem_id": pid,
                "problem_name": pname,
                "tests": combined_tests,
            }
            output_path = os.path.join(OUTPUT, f"{pid}_{safe_name}_gemini_tests.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)
            print(f"  ✔ Saved validated tests to {output_path}")

        except Exception as e:
            print(f"  ✘ Failed: {e}")
            traceback.print_exc(file=sys.stderr)

        time.sleep(5)  # API rate limiting pause


if __name__ == "__main__":
    main()