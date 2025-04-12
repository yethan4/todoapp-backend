from os import name
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

User = settings.AUTH_USER_MODEL



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]
    
    def __str__(self) -> str:
        return self.email

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    task_list = models.ForeignKey('List', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    slug = models.SlugField(primary_key=True, unique=True, db_index=True)
    
    def __str__(self):
        return self.name