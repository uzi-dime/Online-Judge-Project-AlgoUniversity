from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import os
import re
from .service import CompilerService
from problems.models import Problem, TestCase
from solutions.models import Solution, TestResult
from users.auth import jwt_required
from django.conf import settings
compiler_service = CompilerService()

@csrf_exempt
@jwt_required
def compile_and_run(request, problem_id):
    """
    API endpoint to compile and run user-submitted code for a given problem.
    
    Method: POST
    Payload: JSON with keys:
        - 'code': source code (string)
        - 'language': programming language (string)
    
    Response JSON:
        - solution_id: int
        - results: list of test result dicts
        - or error message with appropriate status code.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Parse JSON payload
        data = json.loads(request.body)
        source_code = data.get('code')
        language = data.get('language')
        print(f"Received code for problem {problem_id} in language {language}")
        # Validate required fields
        if not source_code or not language:
            return JsonResponse({'error': 'Code and language are required'}, status=400)

        # Retrieve the problem instance
        problem = get_object_or_404(Problem, pk=problem_id)

        # Load test cases from file matching the problem_id pattern
        test_cases = []
        tests_dir = os.path.join(settings.BASE_DIR, 'solutions', 'cses_tests')
        pattern = re.compile(rf"^{problem_id}_\w+_gemini_tests\.json$")
        for filename in os.listdir(tests_dir):
            if pattern.match(filename):
                filepath = os.path.join(tests_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    test_cases = file_data.get('tests', [])
                break
        
        if not test_cases:
            return JsonResponse({'error': 'Test cases not found for this problem'}, status=404)

        # Run user code against the test cases using your compiler service
        results = compiler_service.run_tests(source_code, language, test_cases)
        # Expected: results is list of objects with attributes like verdict.value, execution_time, etc.

        # Determine overall status for the solution
        for r in results:
            print(r)
            print(f"Test case result: {r.verdict.value}, Time: {r.execution_time}ms, Memory: {r.memory_used}MB")
        all_passed = all(r.verdict.value == 'AC' for r in results)
        solution_status = 'accepted' if all_passed else 'wrong_answer'
        print(f"Solution status: {solution_status}")
        # Create the Solution object representing this submission
        solution = Solution.objects.create(
            problem=problem,
            user=request.user,
            code=source_code,
            language=language,
            status=solution_status
        )

        # Fetch sample test cases from DB, ordered matched with JSON test cases
        db_tests = list(problem.test_cases.order_by('id'))
        if len(db_tests) != len(results):
            print(f"Warning: Expected {len(db_tests)} sample test cases but got {len(results)} results.")
            # Avoid mismatch to prevent data integrity issue
            return JsonResponse({'error': 'Mismatch in test cases and results count'}, status=500)

        # Record each test result linked to the solution
        for result, test_case in zip(results, db_tests):
            TestResult.objects.create(
                solution=solution,
                test_case=test_case,
                status=result.verdict.value,
                execution_time=result.execution_time,
                memory_used=result.memory_used,
                output=result.output,
                error_message=result.error_message
            )

        # Prepare JSON response with solution ID and test results as dictionaries
        response_data = {
            'solution_id': solution.id,
            'results': [r.to_dict() for r in results]  # assuming results implement to_dict()
        }
        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    except Problem.DoesNotExist:
        return JsonResponse({'error': 'Problem not found'}, status=404)
    except Exception as e:
        import traceback
        # Log the exception here (not shown) in production
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=400)


@csrf_exempt
@jwt_required
def submit_solution(request, problem_id):
    """
    Endpoint to submit a solution for evaluation against all test cases
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        source_code = data.get('code')
        language = data.get('language')

        if not source_code or not language:
            return JsonResponse({'error': 'Code and language are required'}, status=400)

        # Create solution record
        solution = Solution.objects.create(
            problem_id=problem_id,
            user=request.user,
            code=source_code,
            language=language,
            status='pending'
        )

        # This would typically trigger an async task to evaluate the solution
        # against all test cases, including hidden ones
        from solutions.tasks import evaluate_solution
        evaluate_solution.delay(solution.id)

        return JsonResponse({
            'solution_id': solution.id,
            'message': 'Solution submitted successfully and is being evaluated'
        }, status=202)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
from django.shortcuts import render

# Create your views here.