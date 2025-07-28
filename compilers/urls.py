from django.urls import path
from . import views

urlpatterns = [
    path('problems/compile/<int:problem_id>/', views.compile_and_run, name='compile_and_run'),
    path('problems/submit/<int:problem_id>/', views.submit_solution, name='submit_solution'),
]
