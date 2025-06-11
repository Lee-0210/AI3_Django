from django.urls import path
from .views import login_view, signup, logout_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login_view'),
    # path('logout/', LogoutView.as_view(next_page='/'), name='logout_view'),
    path('logout/', logout_view, name='logout_view'),
]