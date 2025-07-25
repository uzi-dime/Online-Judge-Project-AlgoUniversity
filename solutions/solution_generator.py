#!/usr/bin/env python3
"""
CSES Solution Generator using Perplexity Pro API
Scrapes CSES problem statements and generates Python solutions using AI
"""

import os
import sys
import json
import time
import shutil
import random
import requests
import traceback
import subprocess
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class CSESSolutionGenerator:
    def __init__(self, perplexity_api_key: str, chromedriver_path: str = "/usr/local/bin/chromedriver"):
        """
        Initialize the CSES Solution Generator
        
        Args:
            perplexity_api_key: Your Perplexity Pro API key
            chromedriver_path: Path to ChromeDriver executable
        """
        self.sample_tests_dir = "cses_sample_tests"  # ADD THIS LINE
        self.api_key = perplexity_api_key
        self.chromedriver_path = chromedriver_path
        self.base_url = "https://cses.fi"
        self.problemset_url = "https://cses.fi/problemset/"
        self.problems_data = []
        self.solutions_dir = "cses_solutions"
        
        # Create solutions directory
        os.makedirs(self.solutions_dir, exist_ok=True)
        os.makedirs(self.sample_tests_dir, exist_ok=True)  # ADD THIS LINE
        
        # Perplexity API settings
        self.api_url = "https://api.perplexity.ai/chat/completions"
        
    def setup_driver(self, headless: bool = True) -> webdriver.Chrome:
        """Setup Chrome WebDriver"""
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
            print(f"Error setting up ChromeDriver: {e}")
            traceback.print_exc()
            return None

    def scrape_problemset(self) -> List[Dict]:
        """Scrape CSES problemset to get problem information"""
        driver = self.setup_driver()
        if not driver:
            return []
        
        try:
            print("Scraping CSES problemset...")
            driver.get(self.problemset_url)
            
            # Wait for page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "task-list"))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            problems = []
            
            # Skip first task-list (usually navigation)
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
            
            print(f"Scraped {len(problems)} problems from CSES")
            self.problems_data = problems
            return problems
            
        except Exception as e:
            print(f"Error scraping problemset: {e}")
            traceback.print_exc()
            return []
        finally:
            if driver:
                driver.quit()

    def extract_sample_test_cases(self, content_div) -> List[Dict[str, str]]:
        """Extract sample input/output test cases from problem statement"""
        test_cases = []
        
        try:
            # Look for sample input/output sections
            sample_sections = content_div.find_all(['h2', 'h3'])
            
            current_input = ""
            current_output = ""
            
            for heading in sample_sections:
                heading_text = heading.get_text().strip().lower()
                
                if 'sample input' in heading_text or 'example input' in heading_text:
                    # Find the next code block or pre element
                    next_elem = heading.find_next_sibling()
                    while next_elem and next_elem.name not in ['pre', 'code', 'h2', 'h3']:
                        next_elem = next_elem.find_next_sibling()
                    
                    if next_elem and next_elem.name in ['pre', 'code']:
                        current_input = next_elem.get_text().strip()
                    elif next_elem and next_elem.name not in ['h2', 'h3']:
                        # Sometimes input is in plain text
                        current_input = next_elem.get_text().strip()
                
                elif 'sample output' in heading_text or 'example output' in heading_text:
                    # Find the next code block or pre element
                    next_elem = heading.find_next_sibling()
                    while next_elem and next_elem.name not in ['pre', 'code', 'h2', 'h3']:
                        next_elem = next_elem.find_next_sibling()
                    
                    if next_elem and next_elem.name in ['pre', 'code']:
                        current_output = next_elem.get_text().strip()
                    elif next_elem and next_elem.name not in ['h2', 'h3']:
                        # Sometimes output is in plain text
                        current_output = next_elem.get_text().strip()
                    
                    # If we have both input and output, save the test case
                    if current_input and current_output:
                        test_cases.append({
                            'input': current_input,
                            'output': current_output
                        })
                        current_input = ""
                        current_output = ""
            
            # Alternative method: look for consecutive pre/code blocks
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
            print(f"Error extracting sample test cases: {e}")
        
        return test_cases


    def save_sample_test_cases(self, problem_id: str, problem_name: str, test_cases: List[Dict[str, str]]):
        """Save sample test cases to JSON file"""
        try:
            if not test_cases:
                print(f"No sample test cases found for {problem_name}")
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
            
            print(f"Saved {len(test_cases)} sample test cases to {filepath}")
            
        except Exception as e:
            print(f"Error saving sample test cases: {e}")


    def scrape_problem_statement(self, problem_url: str) -> Dict[str, str]:
        """Scrape individual problem statement"""
        driver = self.setup_driver()
        if not driver:
            return {}
        
        try:
            driver.get(problem_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "content"))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract problem statement
            content_div = soup.find('div', class_='content')
            if not content_div:
                return {}
            
            # Get problem title
            title = content_div.find('h1')
            title_text = title.text.strip() if title else "Unknown Problem"
            
            # Get problem description
            description_parts = []
            for elem in content_div.find_all(['p', 'ul', 'li']):
                if elem.name == 'p':
                    description_parts.append(elem.get_text().strip())
                elif elem.name == 'ul':
                    for li in elem.find_all('li'):
                        description_parts.append(f"- {li.get_text().strip()}")
            
            description = '\n'.join(description_parts)
            
            # Get input/output format
            input_section = ""
            output_section = ""
            constraints_section = ""
            
            # Look for Input/Output/Constraints sections
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
            
            # Extract sample test cases
            sample_test_cases = self.extract_sample_test_cases(content_div)  # ADD THIS LINE

            return {
                'title': title_text,
                'description': description,
                'input_format': input_section,
                'output_format': output_section,
                'constraints': constraints_section,
                'sample_test_cases': sample_test_cases  # ADD THIS LINE
            }

            
        except Exception as e:
            print(f"Error scraping problem statement: {e}")
            return {}
        finally:
            if driver:
                driver.quit()

    def generate_solution_with_perplexity(self, problem_data: Dict[str, str]) -> str:
        try:
            """Generate Python solution using Perplexity Pro API"""
            # Construct the prompt
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

            Provide only the Python code solution wrapped in python code blocks:"""

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "model": "sonar-pro",
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are an expert competitive programmer specializing in Python solutions for CSES problems. Provide clean, efficient, and correct code.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 2000,
                'temperature': 0.2
            }
            
            print(json.dumps(data, indent=2))
            response = requests.post(self.api_url, headers=headers, json=data)
            print(response.status_code, response.text)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            result = response.json()
            solution = result['choices'][0]['message']['content']
            
            # Extract Python code from response
            code_start = solution.find("```python") + 9
            code_end = solution.find("```", code_start)
            
            if code_start == 8 or code_end == -1:  # 8 means """python wasn't found (-1 + 9)
                print("Error: Could not find valid Python code block in response")
                return ""
                
            solution = solution[code_start:code_end].strip()
            
            if not solution:
                print("Error: Extracted code is empty")
                return ""
                
            return solution
            
        except requests.exceptions.RequestException as e:
            print(f"Perplexity API request failed: {e}")
            return ""
        except KeyError as e:
            print(f"Error parsing API response: Missing key {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error generating solution with Perplexity: {e}")
            traceback.print_exc()
            return ""

    def save_solution(self, problem_id: str, problem_name: str, solution_code: str) -> str:
        """Save solution to file"""
        try:
            # Clean problem name for filename
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
            print(f"Error saving solution: {e}")
            return ""

    def test_solution(self, solution_file: str, test_input: str = None) -> bool:
        """Test solution with sample input"""
        if not test_input:
            return True  # Skip testing if no input provided
        
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
            print(f"Error testing solution: {e}")
            return False

    def generate_solutions_for_category(self, category: str, max_problems: int = 5) -> int:
        """Generate solutions for problems in a specific category"""
        if not self.problems_data:
            print("No problems data available. Run scrape_problemset() first.")
            return 0
        
        category_problems = [p for p in self.problems_data if p['category'].lower() == category.lower()]
        if not category_problems:
            print(f"No problems found for category: {category}")
            return 0
        
        print(f"Generating solutions for {min(max_problems, len(category_problems))} problems in '{category}' category...")
        
        generated_count = 0
        for i, problem in enumerate(category_problems[:max_problems]):
            try:
                print(f"\n[{i+1}/{min(max_problems, len(category_problems))}] Processing: {problem['name']}")
                
                # Scrape problem statement
                problem_statement = self.scrape_problem_statement(problem['url'])
                # Save sample test cases
                if problem_statement.get('sample_test_cases'):
                    self.save_sample_test_cases(
                        problem['id'], 
                        problem['name'], 
                        problem_statement['sample_test_cases']
                    )
                # ADD THESE LINES after: problem_statement = self.scrape_problem_statement(problem['url'])

                if not problem_statement:
                    print(f"Failed to scrape problem statement for {problem['name']}")
                    continue
                
                # Generate solution
                solution = self.generate_solution_with_perplexity(problem_statement)
                if not solution:
                    print(f"Failed to generate solution for {problem['name']}")
                    continue
                
                # Save solution
                filepath = self.save_solution(problem['id'], problem['name'], solution)
                if filepath:
                    print(f"✅ Solution saved: {filepath}")
                    generated_count += 1
                else:
                    print(f"Failed to save solution for {problem['name']}")
                
                # Rate limiting - wait between requests
                time.sleep(2)
                
            except Exception as e:
                print(f"Error processing problem {problem['name']}: {e}")
                continue
        
        print(f"\n🎉 Generated {generated_count} solutions for '{category}' category")
        return generated_count

    def generate_all_solutions(self, max_per_category: int = 3) -> int:
        """Generate solutions for all categories"""
        if not self.problems_data:
            self.scrape_problemset()
        
        if not self.problems_data:
            print("Failed to scrape problems data")
            return 0
        
        categories = list(set(p['category'] for p in self.problems_data))
        print(f"Found {len(categories)} categories: {categories}")
        
        total_generated = 0
        for category in categories:
            try:
                count = self.generate_solutions_for_category(category, max_per_category)
                total_generated += count
                
                # Longer wait between categories
                time.sleep(5)
                
            except Exception as e:
                print(f"Error processing category {category}: {e}")
                continue
        
        print(f"\n🏆 Total solutions generated: {total_generated}")
        return total_generated

    def save_problems_data(self, filename: str = "cses_problems.json"):
        """Save scraped problems data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.problems_data, f, indent=2, ensure_ascii=False)
            print(f"Problems data saved to {filename}")
        except Exception as e:
            print(f"Error saving problems data: {e}")

    def load_problems_data(self, filename: str = "cses_problems.json") -> bool:
        """Load problems data from JSON file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    self.problems_data = json.load(f)
                print(f"Loaded {len(self.problems_data)} problems from {filename}")
                return True
            return False
        except Exception as e:
            print(f"Error loading problems data: {e}")
            return False


def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CSES Solution Generator using Perplexity Pro")
    parser.add_argument("--api-key", required=True, help="Perplexity Pro API key")
    parser.add_argument("--chromedriver", default="/usr/local/bin/chromedriver", 
                       help="Path to ChromeDriver executable")
    parser.add_argument("--category", help="Generate solutions for specific category")
    parser.add_argument("--max-problems", type=int, default=5, 
                       help="Maximum problems per category")
    parser.add_argument("--scrape-only", action="store_true", 
                       help="Only scrape problems, don't generate solutions")
    parser.add_argument("--load-data", help="Load problems from JSON file")
    parser.add_argument("--generate-all", action="store_true", 
                       help="Generate solutions for all categories")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = CSESSolutionGenerator(args.api_key, args.chromedriver)
    
    # Load existing data if specified
    if args.load_data:
        generator.load_problems_data(args.load_data)
    
    # Scrape problems if needed
    if args.scrape_only or not generator.problems_data:
        generator.scrape_problemset()
        generator.save_problems_data()
        if args.scrape_only:
            print("Scraping completed. Exiting.")
            return
    
    def clear_solutions_folder(path: str):
        """
        Delete and recreate the solutions directory to ensure it's empty.
        """
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    def clear_sample_tests_folder(path: str):
        """
        Delete and recreate the sample tests directory to ensure it's empty.
        """
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    clear_sample_tests_folder("cses_sample_tests")  # ADD THIS LINE

    # Generate solutions
    clear_solutions_folder("cses_solutions")
    if args.generate_all:
        generator.generate_all_solutions(args.max_problems)
    elif args.category:
        generator.generate_solutions_for_category(args.category, args.max_problems)
    else:
        print("Use --generate-all or --category to generate solutions")
        print("Available categories:")
        categories = list(set(p['category'] for p in generator.problems_data))
        for cat in categories:
            count = len([p for p in generator.problems_data if p['category'] == cat])
            print(f"  - {cat}: {count} problems")


if __name__ == "__main__":
    main()

