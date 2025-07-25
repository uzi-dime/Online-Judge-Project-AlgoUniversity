from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import json

from .models import Problem, TestCase
from users.auth import jwt_required

@csrf_exempt
@jwt_required
def problem_list(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        difficulty = request.GET.get('difficulty')
        tag = request.GET.get('tag')

        problems = Problem.objects.all()
        if difficulty:
            problems = problems.filter(difficulty=difficulty)
        if tag:
            problems = problems.filter(tags__name=tag)

        paginator = Paginator(problems, per_page)
        page_obj = paginator.get_page(page)

        return JsonResponse({
            'problems': list(page_obj.object_list.values()),
            'total_pages': paginator.num_pages,
            'current_page': page,
            'total_problems': paginator.count
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            problem = Problem.objects.create(
                title=data['title'],
                description=data['description'],
                input_format=data['input_format'],
                output_format=data['output_format'],
                constraints=data['constraints'],
                difficulty=data['difficulty'],
                author=request.user,
                time_limit=data.get('time_limit', 1000),
                memory_limit=data.get('memory_limit', 256)
            )
            
            # Handle tags
            if 'tags' in data:
                problem.tags.add(*data['tags'])
            
            # Handle test cases
            for test_case in data.get('test_cases', []):
                TestCase.objects.create(
                    problem=problem,
                    input_data=test_case['input'],
                    output_data=test_case['output'],
                    is_sample=test_case.get('is_sample', False)
                )
            
            return JsonResponse({
                'id': problem.id,
                'message': 'Problem created successfully'
            }, status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    
    return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
@jwt_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    
    if request.method == 'GET':
        # Check if user has permission to view hidden test cases
        include_hidden = request.user.has_perm('problems.view_hidden_testcases')
        
        data = {
            'id': problem.id,
            'title': problem.title,
            'description': problem.description,
            'input_format': problem.input_format,
            'output_format': problem.output_format,
            'constraints': problem.constraints,
            'difficulty': problem.difficulty,
            'author': {
                'id': problem.author.id,
                'username': problem.author.username
            },
            'created_at': problem.created_at,
            'updated_at': problem.updated_at,
            'time_limit': problem.time_limit,
            'memory_limit': problem.memory_limit,
            'tags': list(problem.tags.values('id', 'name')),
            'sample_test_cases': list(problem.get_sample_test_cases().values(
                'input_data', 'output_data'
            ))
        }
        
        if include_hidden:
            data['hidden_test_cases'] = list(problem.get_hidden_test_cases().values(
                'input_data', 'output_data'
            ))
            
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        if problem.author != request.user and not request.user.is_staff:
            return JsonResponse({'error': 'Not authorized'}, status=403)
            
        try:
            data = json.loads(request.body)
            for field in ['title', 'description', 'input_format', 'output_format', 
                         'constraints', 'difficulty', 'time_limit', 'memory_limit']:
                if field in data:
                    setattr(problem, field, data[field])
            
            if 'tags' in data:
                problem.tags.clear()
                problem.tags.add(*data['tags'])
            
            if 'test_cases' in data:
                # Only staff users can modify hidden test cases
                if not request.user.is_staff:
                    return JsonResponse({'error': 'Not authorized to modify test cases'}, status=403)
                
                problem.test_cases.all().delete()
                for test_case in data['test_cases']:
                    TestCase.objects.create(
                        problem=problem,
                        input_data=test_case['input'],
                        output_data=test_case['output'],
                        is_sample=test_case.get('is_sample', False)
                    )
            
            problem.save()
            return JsonResponse({'message': 'Problem updated successfully'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    
    elif request.method == 'DELETE':
        if problem.author != request.user and not request.user.is_staff:
            return JsonResponse({'error': 'Not authorized'}, status=403)
        problem.delete()
        return JsonResponse({'message': 'Problem deleted successfully'})
    
    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])