from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
import jwt

class SignupToken(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"

class LoginToken:
    @staticmethod
    def generate_token(user):
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def validate_token(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Check if token is expired
            exp = datetime.fromtimestamp(payload['exp'])
            if exp < datetime.utcnow():
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

class CustomTokenAuthentication:
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None

            payload = LoginToken.validate_token(token)
            if not payload:
                return None

            User = get_user_model()
            user = User.objects.get(id=payload['user_id'])
            return (user, token)
        except (ValueError, User.DoesNotExist):
            return None

    def authenticate_header(self, request):
        return 'Bearer'
