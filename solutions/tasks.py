from celery import shared_task
from django.shortcuts import get_object_or_404
from compilers.service import CompilerService

@shared_task
def evaluate_solution(solution_id):
    """
    Asynchronously evaluate a solution against all test cases
    """
    from .models import Solution, TestResult
    from problems.models import TestCase

    # Get the solution
    solution = get_object_or_404(Solution, pk=solution_id)
    
    try:
        # Update status to running
        solution.status = 'running'
        solution.save()

        # Get all test cases for the problem
        test_cases = solution.problem.test_cases.all()
        
        # Initialize compiler service
        compiler_service = CompilerService()
        
        # Track overall metrics
        max_execution_time = 0
        max_memory_used = 0
        all_passed = True
        print(test_cases)  # Debug log
        # Run against each test case
        for test_case in test_cases:
            # Prepare test input
            test_input = {
                'input': test_case.input_data,
                'output': test_case.output_data
            }
            
            # Run the test
            results = compiler_service.run_tests(solution.code, solution.language, [test_input])
            result = results[0]  # We only ran one test case
            
            # Update metrics
            max_execution_time = max(max_execution_time, result.execution_time)
            max_memory_used = max(max_memory_used, result.memory_used)
            
            # Store test result
            TestResult.objects.create(
                solution=solution,
                test_case=test_case,
                status=result.verdict.value,
                execution_time=result.execution_time,
                memory_used=result.memory_used,
                output=result.output,
                error_message=result.error_message
            )
            
            # Check if test passed
            if result.verdict.value != 'AC':
                all_passed = False
                # For hidden test cases, we can stop at first failure
                if not test_case.is_sample:
                    break

        # Update solution status and metrics
        solution.status = 'accepted' if all_passed else 'wrong_answer'
        solution.execution_time = max_execution_time
        solution.memory_used = max_memory_used
        solution.save()

        return {
            'solution_id': solution.id,
            'status': solution.status,
            'execution_time': max_execution_time,
            'memory_used': max_memory_used
        }

    except Exception as e:
        # Update solution status to error
        solution.status = 'runtime_error'
        solution.save()
        
        # Create error test result
        TestResult.objects.create(
            solution=solution,
            test_case=test_cases.first(),
            status='runtime_error',
            error_message=str(e)
        )
        
        return {
            'solution_id': solution.id,
            'status': 'runtime_error',
            'error': str(e)
        }
