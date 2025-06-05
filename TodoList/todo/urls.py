from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todo', views.todo, name='todo'),
    path('create', views.create, name='create'),
    path('delete', views.delete, name='delete'),
    path('ing', views.ing, name='ing'),
    path('done', views.done, name='done'),
    path('cancle', views.cancle, name='cancle'),
]