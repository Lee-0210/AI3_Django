from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post

# Create your views here.
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post/post_detail.html', {'post' : post})