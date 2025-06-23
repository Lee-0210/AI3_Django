from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='index'),
    path('check/', views.checkTodo, name='checkTodo'),
]