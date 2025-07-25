import json
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from users.auth import jwt_required

User = get_user_model()
JWT_SECRET = getattr(settings, 'SECRET_KEY', 'changeme')
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600

def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        user = User.objects.create_user(
            username=username,
            password=password,
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
        )
        user.institution = data.get('institution', '')
        user.country = data.get('country', '')
        user.skill_level = data.get('skill_level', 'BEGINNER')
        user.save()
        token = generate_jwt(user)
        return JsonResponse({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'institution': user.institution,
                'country': user.country,
                'skill_level': user.skill_level
            }
        })
    except Exception as e:
        return HttpResponseBadRequest(str(e))

@csrf_exempt
@jwt_required
def login(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        # data = json.loads(request.body)
        # username = data['username']
        # password = data['password']
        user = request.user
        # user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        token = generate_jwt(user)
        return JsonResponse({'token': token, 'user_id': user.id})
    except Exception as e:
        return HttpResponseBadRequest(str(e))

def hello_user(request):
    return JsonResponse({'message': 'Hello, user!'})
