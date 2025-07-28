from django.db import models
from django.conf import settings

from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class TestCase(models.Model):
    problem = models.ForeignKey('Problem', related_name='test_cases', on_delete=models.CASCADE)
    input_data = models.TextField()
    output_data = models.TextField()
    is_sample = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"TestCase for {self.problem.title} ({'Sample' if self.is_sample else 'Hidden'})"

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    constraints = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='problems')
    tags = models.ManyToManyField(Tag, related_name='problems', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_limit = models.PositiveIntegerField(default=1000, help_text="Time limit in milliseconds")
    memory_limit = models.PositiveIntegerField(default=256, help_text="Memory limit in MB")
    url = models.URLField(blank=True, help_text="URL to the problem statement")

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("view_hidden_testcases", "Can view hidden test cases"),
        ]

    def __str__(self):
        return self.title

    def get_sample_test_cases(self):
        return self.test_cases.filter(is_sample=True)

    def get_hidden_test_cases(self):
        return self.test_cases.filter(is_sample=False)
