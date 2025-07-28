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
    Endpoint to compile and run code against a problem's test cases
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        source_code = data.get('code')
        language = data.get('language')

        if not source_code or not language:
            return JsonResponse({'error': 'Code and language are required'}, status=400)

        # Get the problem and its test cases
        problem = get_object_or_404(Problem, pk=problem_id)
        # Get test cases from file
        test_cases = []
        pattern = re.compile(rf"^{problem_id}_\w+_gemini_tests\.json$")
        for filename in os.listdir(os.path.join(settings.BASE_DIR, 'solutions', 'cses_tests')):
            # print(filename)
            if pattern.match(filename):
                filepath = os.path.join(settings.BASE_DIR, 'solutions', 'cses_tests', filename)
                # print(filepath)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    test_cases = data['tests']
                break
        # print(test_cases)  # Debug log
        # Run the code against test cases
        results = compiler_service.run_tests(source_code, language, test_cases)
        print(f"Results: {results}")  # Debug log
        # Create or update solution record
        solution = Solution.objects.create(
            problem=problem,
            user=request.user,
            code=source_code,
            language=language,
            status='accepted' if all(r.verdict.value == 'AC' for r in results) else 'wrong_answer'
        )

        # Store test results
        for result, test_case in zip(results, problem.test_cases.filter(is_sample=True)):
            TestResult.objects.create(
                solution=solution,
                test_case=test_case,
                status=result.verdict.value,
                execution_time=result.execution_time,
                memory_used=result.memory_used,
                output=result.output,
                error_message=result.error_message
            )

        return JsonResponse({
            'solution_id': solution.id,
            'results': [r.to_dict() for r in results]
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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