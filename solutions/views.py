from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
import json
import os
import re
from django.conf import settings
from .models import Solution, TestResult
from problems.models import Problem, TestCase
from users.auth import jwt_required
from .tasks import evaluate_solution  # We'll create this later for async evaluation
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods


@csrf_exempt
@jwt_required
@require_http_methods(['POST'])
def populate_testcases_all(request):
    """
    Populate test cases for all problems in the cses/tests folder.
    Only accessible by staff users.
    """
    try:
          # Debug log
        print(request.user)
        if request.user.is_staff:
            print('Populating test cases for all problems...')
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        problems = Problem.objects.all()
        created_testcases = []
        for problem in problems:
            # Remove existing test cases
            TestCase.objects.filter(problem=problem).delete()

            pattern = re.compile(rf"^{problem.id}_\w+\.json$")
            for filename in os.listdir(os.path.join(settings.BASE_DIR, 'solutions', 'cses_tests')):
                # print(filename)
                if pattern.match(filename):
                    filepath = os.path.join(settings.BASE_DIR, 'solutions', 'cses_tests', filename)
                    # print(filepath)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        print(data)
                        for tc in data['tests']:
                            testcase = TestCase.objects.create(
                                problem=problem,
                                input_data=tc['input'],
                                output_data=tc['output'],
                                is_sample=tc.get('is_sample', False),
                                # points=tc.get('points', 10)
                            )
                            created_testcases.append({
                                'id': testcase.id,
                                'is_sample': testcase.is_sample,
                                # 'points': testcase.points
                            })
        return JsonResponse({
            'message': f'Successfully created {len(created_testcases)} test cases',
            'testcases': created_testcases
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@jwt_required
def solution_list(request, problem_id=None):
    print("solution_list called")
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        language = request.GET.get('language')
        status = request.GET.get('status')
        user = request.GET.get('user')
        # Base queryset
        if user:
            solutions = Solution.objects.select_related('user', 'problem')
        else:
            solutions = Solution.objects.all()
        # print(f"Initial queryset count: {solutions.count()}")
        # print(solutions)
        # Filter by problem if specified
        if problem_id:
            solutions = solutions.filter(problem_id=problem_id)
        
        # Filter by language if specified
        if language:
            solutions = solutions.filter(language=language)
            
        # Filter by status if specified
        if status:
            solutions = solutions.filter(status=status)
            
        # Users can only see their own solutions unless they have special permission
        # if not request.user.has_perm('solutions.view_all_solutions'):
        #     solutions = solutions.filter(user=request.user)
        
        paginator = Paginator(solutions, per_page)
        page_obj = paginator.get_page(page)
        
        return JsonResponse({
            'solutions': [{
                'id': sol.id,
                'problem': {
                    'id': sol.problem.id,
                    'title': sol.problem.title
                },
                'user': {
                    'id': sol.user.id,
                    'username': sol.user.username
                },
                'language': sol.language,
                'status': sol.status,
                'execution_time': sol.execution_time,
                'memory_used': sol.memory_used,
                'created_at': sol.created_at
            } for sol in page_obj.object_list],
            'total_pages': paginator.num_pages,
            'current_page': page,
            'total_solutions': paginator.count
        })
    
    elif request.method == 'POST':
        if not problem_id:
            return HttpResponseBadRequest("Problem ID is required")
            
        try:
            data = json.loads(request.body)
            problem = get_object_or_404(Problem, pk=problem_id)
            
            # Validate language choice
            if data['language'] not in dict(Solution.LANGUAGE_CHOICES):
                return HttpResponseBadRequest("Invalid language choice")
            
            # Create the solution
            solution = Solution.objects.create(
                problem=problem,
                user=request.user,
                code=data['code'],
                language=data['language']
            )
            
            # Trigger async evaluation
            evaluate_solution.delay(solution.id)
            
            return JsonResponse({
                'id': solution.id,
                'message': 'Solution submitted successfully',
                'status': solution.status
            }, status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    
    return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
@jwt_required
def solution_detail(request, solution_id):
    solution = Solution.objects.filter(pk=solution_id).first()
    if not solution:
        return JsonResponse([], safe=False)
    
    # Check if user has permission to view this solution
    if solution.user != request.user and not request.user.has_perm('solutions.view_all_solutions'):
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    if request.method == 'GET':
        test_results = []
        # Only include sample test results unless user has permission or is the author
        if request.user.has_perm('problems.view_hidden_testcases') or solution.user == request.user:
            test_results = solution.test_results.all()
        else:
            test_results = solution.test_results.filter(test_case__is_sample=True)
        
        return JsonResponse({
            'id': solution.id,
            'problem': {
                'id': solution.problem.id,
                'title': solution.problem.title
            },
            'user': {
                'id': solution.user.id,
                'username': solution.user.username
            },
            'code': solution.code,
            'language': solution.language,
            'status': solution.status,
            'execution_time': solution.execution_time,
            'memory_used': solution.memory_used,
            'created_at': solution.created_at,
            'updated_at': solution.updated_at,
            'test_results': [{
                'status': result.status,
                'execution_time': result.execution_time,
                'memory_used': result.memory_used,
                'output': result.output if result.test_case.is_sample else None,
                'error_message': result.error_message if result.test_case.is_sample else None
            } for result in test_results]
        })
    
    elif request.method == 'PUT':
        # Only allow updating code and language, and only if solution is pending or has error
        if solution.user != request.user:
            return JsonResponse({'error': 'Not authorized'}, status=403)
        
        if solution.status not in ['pending', 'compilation_error']:
            return JsonResponse({'error': 'Cannot modify submitted solution'}, status=400)
            
        try:
            data = json.loads(request.body)
            
            if 'language' in data:
                if data['language'] not in dict(Solution.LANGUAGE_CHOICES):
                    return HttpResponseBadRequest("Invalid language choice")
                solution.language = data['language']
                
            if 'code' in data:
                solution.code = data['code']
                
            solution.status = 'pending'
            solution.save()
            
            # Re-trigger evaluation
            evaluate_solution.delay(solution.id)
            
            return JsonResponse({'message': 'Solution updated and queued for evaluation'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    
    elif request.method == 'DELETE':
        # Only allow deletion if user is author or staff
        if solution.user != request.user and not request.user.is_staff:
            return JsonResponse({'error': 'Not authorized'}, status=403)
            
        solution.delete()
        return JsonResponse({'message': 'Solution deleted successfully'})
    
    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])


@csrf_exempt
@jwt_required
def testcase_list(request, problem_id):
    """
    List all test cases for a given problem
    """
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
        
    test_cases = TestCase.objects.filter(problem_id=problem_id)
    
    return JsonResponse({
        'test_cases': [{
            'id': t.id,
            'problem': {
                'id': t.problem.id,
                'title': t.problem.title
            },
            'input_data': t.input_data,
            'output_data': t.output_data
        } for t in test_cases]
    })
