from django.urls import path
from . import views

urlpatterns = [
    path('solutions/', views.solution_list, name='solution_list'),
    path('solutions/<int:solution_id>/', views.solution_detail, name='solution_detail'),
    path('problems/<int:problem_id>/solutions/', views.solution_list, name='problem_solutions'),
]
