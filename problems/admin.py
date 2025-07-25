from django.contrib import admin
from .models import Problem  # Assuming you have a Problem model in models.py

admin.site.register(Problem)  # Register the Problem model with the admin site