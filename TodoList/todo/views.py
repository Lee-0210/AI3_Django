from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *      # models 의 모든 모델 import
from django.db.models import Q

# Create your views here.
def index(request):
    print("메인 화면...")
    return render(request, 'todo/index.html', {})

def todo(request):
    print("할 일 목록 화면...")
    # 할 일 목록 조회
    # Todo 모델의 대기 목록 조회
    wait_list = Todo.objects.filter(status='WAIT')
    # Todo 모델의 진행 목록 조회
    ing_list = Todo.objects.filter(Q(status='ING') | Q(status='DONE')).order_by('-status')

    content = {'wait_list' : wait_list, 'ing_list' : ing_list}
    # render(request, 템플릿 경로, 데이터{})
    # - 데이터{} : 템플릿에 데이터를 전달
    return render(request, 'todo/todo.html', content)

def create(request):
    print("할 일 등록...")
    # POST 방식의 파라미터
    title = request.POST['title']
    # 등록 요청
    new_todo = Todo(title=title)
    new_todo.save()     # DB에 저장
    # 할 일 목록으로 리다이렉트
    return HttpResponseRedirect(reverse('todo'))

def delete(request):
    print("삭제 요청...")
    # 파라미터
    no = request.POST['no']
    print(f"삭제할 no : {no}")
    try:
        todo = Todo.objects.get(no=no)
        todo.delete()   # 할 일 삭제 요청
    except Todo.DoesNotExist:
        print("삭제할 할 일이 없습니다.")
    return HttpResponseRedirect(reverse('todo'))

def ing(request):
    print("진행 상태로 변경...")
    # 파라미터
    no = request.POST['no']
    print(f"수정할 no : {no}")
    try:
        todo = Todo.objects.get(no=no)
        # 할 일 상태 수정
        todo.status = 'ING'
        todo.save()
    except Todo.DoesNotExist:
        print("수정할 할 일이 없습니다.")
    return HttpResponseRedirect(reverse('todo'))

def done(request):
    print("완료 상태로 변경...")
    # 파라미터
    no = request.POST['no']
    print(f"완료 처리할 no : {no}")
    try:
        todo = Todo.objects.get(no=no)
        # 할 일 상태 수정
        if todo.status == 'DONE':
            todo.status = 'ING'
        else:
            todo.status = 'DONE'
        todo.save()
    except Todo.DoesNotExist:
        print("완료로 변경할 일이 없습니다.")
    return HttpResponseRedirect(reverse('todo'))

# 다시 대기로 변경
def cancle(request):
    print("대기 상태로 변경...")
    # 파라미터
    no = request.POST['no']
    print(f"대기 처리할 no : {no}")
    try:
        todo = Todo.objects.get(no=no)
        todo.status = 'WAIT'
        todo.save()
    except Todo.DoesNotExist:
        print("완료로 변경할 일이 없습니다.")
    return HttpResponseRedirect(reverse('todo'))

