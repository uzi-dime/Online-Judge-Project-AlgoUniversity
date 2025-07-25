from django.db import models
from django.conf import settings

class Solution(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('javascript', 'JavaScript'),
        ('golang', 'Go'),
        ('rust', 'Rust')
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('accepted', 'Accepted'),
        ('wrong_answer', 'Wrong Answer'),
        ('time_limit', 'Time Limit Exceeded'),
        ('memory_limit', 'Memory Limit Exceeded'),
        ('runtime_error', 'Runtime Error'),
        ('compilation_error', 'Compilation Error')
    ]

    problem = models.ForeignKey('problems.Problem', on_delete=models.CASCADE, related_name='solutions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solutions')
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    execution_time = models.FloatField(null=True, blank=True)  # in milliseconds
    memory_used = models.FloatField(null=True, blank=True)    # in MB
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("view_all_solutions", "Can view all solutions"),
        ]

    def __str__(self):
        return f"{self.user.username}'s solution for Problem {self.problem.title}"

class TestResult(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='test_results')
    test_case = models.ForeignKey('problems.TestCase', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Solution.STATUS_CHOICES)
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.FloatField(null=True, blank=True)
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        unique_together = ('solution', 'test_case')
        ordering = ['test_case__created_at']