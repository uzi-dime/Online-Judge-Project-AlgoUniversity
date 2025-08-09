from django.core.management.base import BaseCommand
from django.conf import settings
from problems.models import Problem

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
from typing import List, Dict, Optional


class CSESTestGenerator:
    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr
        self.api_key = getattr(settings, "GEMINI_API_KEY", None)
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY missing in settings.py")
        
        # Constants and Paths
        self.base_dir = settings.BASE_DIR
        self.model = "gemini-2.5-flash-lite"
        self.problems_file = os.path.join(self.base_dir, "solutions", "cses_problems.json")
        self.output_dir = os.path.join(self.base_dir, "solutions", "cses_tests")
        self.sample_tests_dir = os.path.join(self.base_dir, "solutions", "cses_sample_tests")
        self.solutions_dir = os.path.join(self.base_dir, "solutions", "cses_solutions")
        
        self.prompt_template = """
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

Use the above solution code to generate {small} small and {large} large test cases. For each test case:

- Provide the input.
- Compute the expected output exactly as the solution would produce it.
- Format all test cases EXACTLY as a JSON array of objects with keys "size", "input", and "output".
- Return ONLY the JSON array, no explanations or additional text.
"""

    def load_problems(self) -> List[Dict]:
        """Load problems from JSON file, filtered by those existing in the database."""
        problems_path = os.path.join(self.base_dir, "solutions", self.problems_file)
        if not os.path.exists(problems_path):
            self.stderr.write(f"Problems file not found: {problems_path}")
            return []
        
        with open(problems_path, encoding="utf-8") as f:
            json_problems = json.load(f)

        problem_ids_in_db = set(Problem.objects.values_list('id', flat=True))
        # print(f"Found {problem_ids_in_db} problems in the database")
        # print(f"Loaded {len(json_problems)} problems from JSON file, {json_problems} in total")
        filtered_problems = [problem for problem in json_problems if int(problem['id']) in problem_ids_in_db]
        
        self.stdout.write(f"Loaded {len(filtered_problems)} problems from database")
        return filtered_problems

    def scrape_statement(self, url: str) -> tuple:
        """Scrape problem statement from CSES URL."""
        try:
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
        except Exception as e:
            self.stderr.write(f"Error scraping statement from {url}: {e}")
            return "", "", "", "", ""

    def find_sample_test_file(self, problem_id_prefix: str) -> Optional[str]:
        """Find sample test file for a given problem ID prefix."""
        pattern = os.path.join(self.sample_tests_dir, f"{problem_id_prefix}*.json")
        matching_files = glob.glob(pattern)
        if not matching_files:
            return None
        return matching_files[0]

    def load_sample_tests(self, problem_id: str) -> Optional[Dict]:
        """Load sample tests for a problem."""
        prefix = problem_id.split("_")[0]
        sample_test_file = self.find_sample_test_file(prefix)
        if not sample_test_file:
            return None
        try:
            with open(sample_test_file, encoding="utf-8") as f:
                data = json.load(f)
            if data.get("problem_id") and not data["problem_id"].startswith(prefix):
                self.stdout.write(f"Warning: sample test file {sample_test_file} problem_id mismatch")
            return data
        except Exception as e:
            self.stdout.write(f"Warning: Failed to load sample tests from {sample_test_file}: {e}")
            return None

    def format_sample_tests_for_prompt(self, sample_data: Optional[Dict]) -> str:
        """Format sample tests for inclusion in the prompt."""
        if not sample_data or "test_cases" not in sample_data:
            return "No sample tests available."

        lines = []
        for i, testcase in enumerate(sample_data["test_cases"], 1):
            inp = testcase.get("input", "").replace('\n', '\\n')
            outp = testcase.get("output", "").replace('\n', '\\n')
            lines.append(f"Sample Test #{i}:\nInput: {inp}\nOutput: {outp}")
        return "\n\n".join(lines)

    def extract_json_array(self, text: str) -> str:
        """Extract JSON array from model response text."""
        text = text.strip()
        while text.startswith("```") and text.endswith("```"):
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

    def read_solution_code(self, problem_id: str, problem_name: str) -> Optional[str]:
        """Read solution code content for embedding in prompt."""
        safe_name = re.sub(r"[^\w\d-]+", "_", problem_name)
        solution_path = os.path.join(self.solutions_dir, f"{problem_id}_{safe_name}.py")
        
        if os.path.isfile(solution_path):
            try:
                with open(solution_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                self.stdout.write(f"Warning: Could not read solution code for {problem_id}: {e}")
                return None
        
        glob_candidates = glob.glob(os.path.join(self.solutions_dir, f"{problem_id}_*.py"))
        if glob_candidates:
            try:
                with open(glob_candidates[0], "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                self.stdout.write(f"Warning: Could not read solution code for {problem_id}: {e}")
        return None

    def find_solution_script_path(self, problem_id: str, problem_name: str) -> Optional[str]:
        """Find filesystem path to solution script for validation."""
        safe_name = re.sub(r"[^\w\d-]+", "_", problem_name)
        solution_path = os.path.join(self.solutions_dir, f"{problem_id}_{safe_name}.py")
        
        if os.path.isfile(solution_path):
            return solution_path
        
        candidates = glob.glob(os.path.join(self.solutions_dir, f"{problem_id}_*.py"))
        if candidates:
            return candidates[0]
        return None

    def generate_gemini_tests(self, problem: Dict, llm, small: int = 10, large: int = 10, 
                            sample_tests_data: Optional[Dict] = None, retries: int = 2) -> List[Dict]:
        """Generate test cases using Gemini API."""
        title, desc, inp, outp, cons = self.scrape_statement(problem["url"])
        sample_tests_text = self.format_sample_tests_for_prompt(sample_tests_data)
        solution_code = self.read_solution_code(problem["id"], problem["name"])

        if not solution_code:
            self.stdout.write(f"⚠️ Warning: No solution code found for problem {problem['id']} - {problem['name']}")

        prompt = self.prompt_template.format(
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
                json_text = self.extract_json_array(text)
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
                    self.stdout.write(f"  ✗ Attempt {attempt+1} failed, retrying after {wait_time}s... Error: {e}")
                    time.sleep(wait_time)
                else:
                    self.stderr.write(f"  ✘ Failed to generate tests for problem {problem['id']} after {retries + 1} attempts: {e}")
                    traceback.print_exc()

        return []

    def run_solution_on_input(self, solution_path: str, input_str: str, timeout: int = 5) -> Optional[str]:
        """Run solution script on given input and return output."""
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
                self.stdout.write(f"⚠️ Solution exited with return code {proc.returncode}")
                if proc.stderr.strip():
                    self.stdout.write(f"stderr:\n{proc.stderr.strip()}")
                return None
            if output == "":
                if proc.stderr.strip():
                    self.stdout.write(f"⚠️ Solution stderr (no stdout):\n{proc.stderr.strip()}")
                else:
                    self.stdout.write(f"⚠️ Solution produced empty output for input:\n{input_str}")
                return None
            return output
        except subprocess.TimeoutExpired:
            self.stdout.write(f"⚠️ Solution timed out on input:\n{input_str}")
        except Exception as e:
            self.stdout.write(f"⚠️ Error running solution on input:\n{input_str}\nError: {e}")
        return None

    def validate_test_cases(self, solution_path: str, test_cases: List[Dict]) -> List[Dict]:
        """Validate test cases against solution script."""
        if not solution_path:
            self.stdout.write("⚠️ No solution script found, skipping validation.")
            return test_cases

        valid_cases = []
        for idx, test_case in enumerate(test_cases, 1):
            inp = test_case["input"]
            expected_output = test_case["output"].strip()
            actual_output = self.run_solution_on_input(solution_path, inp)
            if actual_output is None:
                self.stdout.write(f"  ✗ Test case #{idx}: execution failed, discarding.")
                continue
            if actual_output == expected_output:
                valid_cases.append(test_case)
            else:
                self.stdout.write(f"  ✗ Test case #{idx}: output mismatch.\nExpected: {expected_output!r}\nActual:   {actual_output!r}")
        
        self.stdout.write(f"  ✔ Validation complete: {len(valid_cases)} / {len(test_cases)} test cases passed.")
        return valid_cases

    def generate_tests_for_problems(self, problems: List[Dict], small_tests: int = 10, large_tests: int = 10):
        """Generate tests for all problems."""
        genai.configure(api_key=self.api_key)
        llm = genai.GenerativeModel(self.model)

        # Clean and create output directory
        output_path = os.path.join(self.base_dir, self.output_dir)
        # if os.path.exists(output_path):
        #     shutil.rmtree(output_path)
        # os.makedirs(output_path, exist_ok=True)

        for problem in problems:
            pid = problem["id"]
            pname = problem["name"]
            safe_name = re.sub(r"[^\w\d-]+", "_", pname)

            self.stdout.write(f"Generating Gemini AI tests for {pid}_{safe_name} ...")

            sample_tests_data = self.load_sample_tests(pid)
            if sample_tests_data:
                self.stdout.write(f"  ✔ Loaded sample tests from {sample_tests_data.get('problem_id')}")

            try:

                test_output_path = os.path.join(output_path, f"{pid}_{safe_name}_gemini_tests.json")

                if os.path.exists(test_output_path):
                    with open(test_output_path, "r", encoding="utf-8") as f:
                        existing_data = json.load(f)
                        if len(existing_data.get("tests", [])) >= 5:
                            self.stdout.write(f"  ✔ Test file {test_output_path} already contains 5 or more test cases. Skipping generation.")
                            continue

                generated_tests = self.generate_gemini_tests(
                    problem, llm, small=small_tests, large=large_tests, sample_tests_data=sample_tests_data
                )

                combined_tests = []
                if sample_tests_data and "test_cases" in sample_tests_data:
                    for st in sample_tests_data["test_cases"]:
                        combined_tests.append({
                            "size": "sample",
                            "input": st["input"],
                            "output": st["output"],
                        })
                combined_tests.extend(generated_tests)

                solution_script_path = self.find_solution_script_path(pid, pname)
                if solution_script_path:
                    self.stdout.write(f"  ✔ Validating all test cases against solution script at {solution_script_path} ...")
                    combined_tests = self.validate_test_cases(solution_script_path, combined_tests)
                else:
                    self.stdout.write("⚠️ No solution script file found. Skipping validation.")

                output_data = {
                    "problem_id": pid,
                    "problem_name": pname,
                    "tests": combined_tests,
                }
                
                with open(test_output_path, "w", encoding="utf-8") as f:
                    json.dump(output_data, f, indent=2)
                self.stdout.write(f"  ✔ Saved validated tests to {test_output_path}")

            except Exception as e:
                self.stderr.write(f"  ✘ Failed: {e}")
                traceback.print_exc()

            time.sleep(5)  # API rate limiting pause


class Command(BaseCommand):
    help = "Generate test cases for CSES problems using Gemini API"

    def add_arguments(self, parser):
        parser.add_argument(
            '--small-tests', type=int, default=10,
            help='Number of small test cases to generate per problem'
        )
        parser.add_argument(
            '--large-tests', type=int, default=10,
            help='Number of large test cases to generate per problem'
        )
        parser.add_argument(
            '--problem-ids', nargs='+',
            help='Specific problem IDs to generate tests for (optional)'
        )

    def handle(self, *args, **options):
        small_tests = options['small_tests']
        large_tests = options['large_tests']
        specific_problem_ids = options.get('problem_ids')

        try:
            generator = CSESTestGenerator(self.stdout, self.stderr)
            
            # Load problems
            problems = generator.load_problems()
            if not problems:
                self.stderr.write("No problems found to process.")
                return

            # Filter by specific problem IDs if provided
            if specific_problem_ids:
                problems = [p for p in problems if p['id'] in specific_problem_ids]
                self.stdout.write(f"Filtered to {len(problems)} specific problems")

            if not problems:
                self.stderr.write("No problems match the specified criteria.")
                return

            # Clean any existing test files
            pattern = re.compile(r"^(\d+)_(.+)_gemini_tests\.json$")
            for filename in os.listdir(generator.base_dir):
                match = pattern.match(filename)
                if match:
                    problem_id, problem_name = match.groups()
                    if problem_id not in [p['id'] for p in problems]:
                        file_path = os.path.join(generator.base_dir, filename)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                                self.stdout.write(f"  ✔ Removed existing test file: {file_path}")
                        except Exception as e:
                            self.stderr.write(f"  ✘ Failed to delete {file_path}. {e}")
                
            self.stdout.write(f"Starting test generation for {len(problems)} problems...")
            self.stdout.write(f"Small tests per problem: {small_tests}")
            self.stdout.write(f"Large tests per problem: {large_tests}")

            # Generate tests
            generator.generate_tests_for_problems(problems, small_tests, large_tests)
            
            self.stdout.write(self.style.SUCCESS("✅ Test generation completed successfully!"))

        except ValueError as e:
            self.stderr.write(f"Configuration error: {e}")
        except Exception as e:
            self.stderr.write(f"Unexpected error: {e}")
            traceback.print_exc()