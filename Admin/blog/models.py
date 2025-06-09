from django.db import models
from django.contrib.auth.models import AbstractUser
from slugify import slugify
# Create your models here.

# 커스텀 User 모델
class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set', # 역참조 이름 지정
    )
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set', # 역참조 이름 지정
    )

# 게시글 모델 - Post
# related_name 속성
# - CustomUser 모델에서 posts 속성을 통해 Post 모델에 접근할 수 있게 한다.
# - related_name 을 지정하지 않으면, Django 는 기본적으로 'post_set' 이라는 이름을 사용한다.
class Post(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    user        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    is_public   = models.BooleanField(default=True)

    # 모델의 save() 함수를 오버라이딩하여, slugify() 적용
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # slugify() 함수는 문자열을 URL-friendly 한 형식으로 변환한다.
        super().save(*args, **kwargs)

# 댓글 모델 - Comments
class Comment(models.Model):
    post        = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)


