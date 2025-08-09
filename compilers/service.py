from .python_compiler import PythonCompiler
from .base import Verdict, CompilerResult

class CompilerService:
    def __init__(self):
        self.compilers = {
            'python': PythonCompiler(),
            # Add more compilers here
        }

    def get_compiler(self, language):
        return self.compilers.get(language)

    def run_tests(self, source_code, language, test_cases):
        """
        Run the solution against all test cases
        Returns a list of CompilerResult objects
        """
        compiler = self.get_compiler(language)
        if not compiler:
            return [CompilerResult(
                Verdict.COMPILATION_ERROR,
                error_message=f"Unsupported language: {language}"
            )]

        # First, try to compile the code
        compile_result = compiler.compile(source_code)
        if compile_result.verdict == Verdict.COMPILATION_ERROR:
            return [compile_result]

        # Run each test case
        results = []
        for test_case in test_cases:
            result = compiler.run(source_code, test_case['input'])
            print(result.output, test_case['output'])
            # Check if output matches expected output
            if result.verdict == Verdict.ACCEPTED:
                expected_output = test_case['output'].strip()
                actual_output = result.output.strip()
                
                if actual_output != expected_output:
                    result.verdict = Verdict.WRONG_ANSWER
                    result.error_message = "Output doesn't match expected output"
            
            results.append(result)

        return results
