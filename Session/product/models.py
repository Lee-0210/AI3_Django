from django.db import models

# Create your models here.
class Product(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    # max_digits     : 숫자 최대 자리수 (정수+소수 : 10자리)
    # decimal_places : 소수점 이하 자리수 (소수 둘째 자리)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField()
    img         = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)