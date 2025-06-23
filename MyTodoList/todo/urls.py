from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('change/', views.change, name='change'),
    path('success/<int:id>', views.success, name='success'),
    path('remove/<int:id>', views.remove, name='remove'),
]