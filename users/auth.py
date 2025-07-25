import jwt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from functools import wraps


User = get_user_model()
JWT_SECRET = getattr(settings, 'SECRET_KEY', 'your-secret-key')
JWT_ALGORITHM = 'HS256'

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return JsonResponse({'error': 'No token provided'}, status=401)
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user = User.objects.get(id=payload['user_id'])
            request.user = user
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        return view_func(request, *args, **kwargs)
    return wrapper
