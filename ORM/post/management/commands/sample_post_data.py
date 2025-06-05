from post.models import Post
from django.utils import timezone

for i in range(1, 11):
    Post.objects.create(
        title=f"title {i}",
        writer=f"user{i}",
        content=f"{i} content",
        created_at=timezone.now(),
        updated_at=timezone.now()
    )