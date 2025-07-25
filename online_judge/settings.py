# settings.py (relevant excerpts)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps (if any)...

    # Local apps
    'problems',
    'solutions',
    'compilers',
    'users',

    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True  # For development; restrict in production
CORS_ALLOWED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]  #

ROOT_URLCONF = 'online_judge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'online_judge.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Specify the custom user model
AUTH_USER_MODEL = 'users.User'

# Password validation…
AUTH_PASSWORD_VALIDATORS = [
    # validators...
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# /home/flash/projects/online-judge/online_judge/settings.py
# ... (other settings)

GEMINI_API_KEY = "AIzaSyAVX6va96s6iwvjBtivSR1aUB0tFbsw95k"  # Replace with your actual key
CSES_SCRAPE_DELAY = 1.0
GEMINI_MODEL = "gemini-1.5-flash"

# settings.py (relevant section)
import os
from pathlib import Path

# BASE_DIR is the Django project root (e.g., /path/to/online-judge)
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files configuration
STATIC_URL = '/static/'  # URL prefix for serving static files (e.g., /static/assets/js/api.js)

# Directories where Django looks for static files
STATICFILES_DIRS = [
    # Points to sibling directory: e.g., /path/to/online-judge-frontend/static
    BASE_DIR.parent / 'online-judge-frontend' / 'static',
    # Add more if needed, e.g., BASE_DIR / 'additional_static_folder'
]

print(f"Static files will be served from: {STATICFILES_DIRS}")

# For production: Where collectstatic copies files to
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Ensure DEBUG is True for development (allows runserver to serve static files)
DEBUG = True
