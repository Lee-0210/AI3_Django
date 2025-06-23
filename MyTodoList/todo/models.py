from django.db import models

# Create your models here.
class Todo(models.Model):
    STATUS_CHOICE = [
        ('WAIT', '대기'),
        ('ING', '진행'),
    ]

    title = models.CharField(null=False, blank=False, max_length=200)
    content = models.TextField(blank=True)
    status = models.CharField(
                        max_length=20,
                        choices=STATUS_CHOICE,
                        default='WAIT'
                        )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title : {self.title}, content : {self.content}, is_completed : {self.is_completed}"