import os  # <--- Add this line
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_judge.settings')

application = get_wsgi_application()