from django.urls import path
from . import views

urlpatterns = [
    path('problems/<int:problem_id>/compile/', views.compile_and_run, name='compile_and_run'),
    path('problems/<int:problem_id>/submit/', views.submit_solution, name='submit_solution'),
]
