from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
  nickname = models.CharField(max_length=30, blank=True, null=True)
  gender = models.CharField(max_length=10, blank=True, null=True)
  age = models.PositiveIntegerField(blank=True, null=True)

  user_permissions = models.ManyToManyField(
    'auth.Permission',
    verbose_name='user permissions',
    blank=True,
    help_text='Specific permissions for this user.',
    related_name='custom_user_set',  # 역참조 이름 지정
  )
  groups = models.ManyToManyField(
    'auth.Group',
    verbose_name='groups',
    blank=True,
    help_text='The groups this user belongs to.',
    related_name='custom_user_set',  # 역참조 이름 지정
  )