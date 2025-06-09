from django.contrib import admin
from django.forms import Textarea
from django.db import models
from blog.models import Comment, CustomUser, Post

# Register your models here.
"""
    Django Amdin 에서 모델을 관리하기 위한 설정 파일
    * 관리자 등록 방법
    1. admin.site.register(모델명)
    * 커스텀 : 설정 class 를 만들어서 등록할 수 있다.
    * class XXXAdmin(설정 클래스):
    * admin.site.register(모델명, XXXAdmin)
    2. @admin.register(모델명) 데코레이터 사용
"""
# 방법 1 : admin.site.register()
class CustomUserAdmin(admin.ModelAdmin):
    # 출력 필드 설정
    list_display    = ('username', 'nickname', 'email', 'is_staff', 'is_active')
    # 검색 필드 설정
    search_fields   = ('username', 'nickname', 'email')
    # 필터링 설정
    list_filter     = ('is_staff', 'is_active')

# class PostAdmin(admin.ModelAdmin):
#     # 출력 필드 설정
#     list_display    = ('post_title', 'user_nickname', 'content', 'post_created_at', 'post_updated_at', 'slug')
#     # 읽기 전용 필드 설정
#     readonly_fields = ('created_at', 'updated_at')

#     # post -> user 필드에서 CustomUser 모델의 nickname 을 표시하기 위한 함수
#     # * 함수 이름 : 출력 필드 이름과 동일하게 설정
#     def post_title(self, obj):
#         return obj.title
#     post_title.short_description = '제목'

#     def user_nickname(self, obj):
#         return obj.user.nickname if obj.user else 'Unknown'
#     user_nickname.short_description = '닉네임' # 츨력 필드 이름 설정

#     def post_created_at(self, obj):
#         fm_date = obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
#         return fm_date
#     post_created_at.short_description = '생성날짜'

#     def post_updated_at(self, obj):
#         fm_date = obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
#         return fm_date
#     post_updated_at.short_description = '수정날짜'

#     # 자동 슬러그 생성
#     prepopulated_fields = {'slug' : ('title',)}

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

# 방법 2 : @admin.register(모델명)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 출력 필드 설정
    list_display    = ('is_public', 'post_title', 'user_nickname', 'content', 'post_created_at', 'post_updated_at', 'slug', 'comment_count')
    # 읽기 전용 필드 설정
    readonly_fields = ('created_at', 'updated_at')

    # post -> user 필드에서 CustomUser 모델의 nickname 을 표시하기 위한 함수
    # * 함수 이름 : 출력 필드 이름과 동일하게 설정
    def post_title(self, obj):
        return obj.title
    post_title.short_description = '제목'

    def user_nickname(self, obj):
        return obj.user.nickname if obj.user else 'Unknown'
    user_nickname.short_description = '닉네임' # 츨력 필드 이름 설정

    def post_created_at(self, obj):
        fm_date = obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return fm_date
    post_created_at.short_description = '생성날짜'

    def post_updated_at(self, obj):
        fm_date = obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        return fm_date
    post_updated_at.short_description = '수정날짜'

    def comment_count(self, obj):
        return obj.comments.count() if obj.comments else 0
    comment_count.short_description = '댓글 수'
    # 자동 슬러그 생성
    prepopulated_fields = {'slug' : ('title',)}

    # 액션 설정
    # * 정의한 액션 메서드를 actions 에 추가하여
    # 관리자 페이지에서 사용할 수 있도록 한다.
    actions = ['make_public']

    @admin.action(description='일괄 공개 처리')
    def make_public(self, request, querset):
        querset.update(is_public=True)

    # 위젯 커스터마이징
    formfield_overrides = {
        models.TextField: {'widget' : Textarea(attrs={'rows' : 3, 'cols' : 60})}
    }

    # 인라인 모델 설정
    inlines = [CommentInline]