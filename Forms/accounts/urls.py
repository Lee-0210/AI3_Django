# accounts/urls.py
from django.urls import path
from .views import signup_view
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
]
