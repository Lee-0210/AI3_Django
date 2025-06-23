from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(null=False, blank=False, max_length=200)
    content = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title : {self.title}, content : {self.content}, is_completed : {self.is_completed}"