from django.db import models

from django.conf import settings

User = settings.AUTH_USER_MODEL

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title