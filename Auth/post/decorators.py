from django.core.exceptions import PermissionDenied
from functools import wraps
from .models import Post

def user_is_post_owner(view_func):
    @wraps(view_func)
    def _wrapped_view(request, post_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)
        if post.user != request.user and not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, post_id, *args, **kwargs)

    return _wrapped_view