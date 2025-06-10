
from django.contrib import admin
from django.urls import include, path
from post.views import index

urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
