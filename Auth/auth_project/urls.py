
from django.contrib import admin
from django.urls import include, path
from post.views import index, callback

urlpatterns = [
    path('', index, name='index'),
    path('callback/', callback, name='callback'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('post/', include('post.urls', namespace='post'))
]
