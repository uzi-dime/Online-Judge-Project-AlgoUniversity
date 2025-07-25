import json
import glob
import os

def analyze_test_files():
    # Path to test files
    test_files = glob.glob('cses_tests/*_tests.json')
    
    empty_input_problems = []
    total_files = 0
    
    for file_path in test_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                total_files += 1
                
                for test in data.get('tests', []):
                    # print(test.get('input'))
                    if test.get('input') == "":
                        empty_input_problems.append(data.get('problem_id'))
                        break
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Print results
    print(f"\nTotal test files analyzed: {total_files}")
    print(f"Number of problems with empty input: {len(empty_input_problems)}")
    print("\nProblems with empty input:")
    for prob in empty_input_problems:
        print(f"Problem ID: {prob}")

if __name__ == "__main__":
    analyze_test_files()
