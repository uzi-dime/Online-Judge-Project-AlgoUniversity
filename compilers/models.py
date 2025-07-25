from django.db import models

class Compiler(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    executable_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.version})"