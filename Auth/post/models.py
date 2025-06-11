from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # 중요: AUTH_USER_MODEL 접근을 위해 필요

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
