import os  # <--- Add this line
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')

application = get_asgi_application()