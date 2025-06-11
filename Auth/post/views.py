from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .decorators import user_is_post_owner

# Create your views here.
def index(request):
    return render(request, 'post/index.html')

def list_view(request):
    posts = Post.objects.all()
    return render(request, 'post/list.html', {'posts' : posts})

# 게시글 등록
@login_required
def create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post:list')
        else:
            # 폼 유효성 검사 실패 시 여러 메시지 추가
            form.add_error(None, '게시글 작성에 실패하였습니다. 다시 시도해주세요.')
    else:
        form = PostForm()
    return render(request, 'post/create.html', {'form' : form})

# 게시글 조회
def read_view(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post/read.html', {'post' : post})

# 게시글 수정
@login_required         # 로그인 검증
@user_is_post_owner     # 소유자 검증
def update_view(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post:read', post_id = post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'post/update.html', {'form' : form, 'post' : post})

# 게시글 삭제
@login_required
@user_is_post_owner
def delete_view(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post:list')

    # 게시글 삭제 실패
    return redirect('post:update', post_id=post.id)
