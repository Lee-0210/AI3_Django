from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q
from .forms import TodoForm
from .models import Todo
from django.views.decorators.http import require_http_methods

# 인덱스 페이지
def index(request):
    return render(request, 'index.html')

# Todo List 페이지
def list(request):
    # 대기중 리스트
    list = Todo.objects.filter(Q(status='WAIT') & Q(is_completed=False))
    # 진행중 리스트
    ing_list = Todo.objects.filter(Q(status='ING') & Q(is_completed=False))
    # 완료 리스트
    done_list = Todo.objects.filter(is_completed=True)
    # 그냥 폼
    form = TodoForm()
    # title 미입력시 error 파라미터 전달
    error = request.GET.get('error')
    return render(request, 'list.html', {"list" : list, 'form' : form, 'error' : error, 'done_list' : done_list, 'ing_list' : ing_list})

# Todo 등록
def create(request):
    # 내부에서 HTTP 메서드 나누기
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo:list')
        else:
            # 유효성 검사 실패시 list 로 리다이렉트
            url = reverse('todo:list') + '?error=1'
            return redirect(url)
    else:
        return redirect('todo:list')

# 대기 / 진행 전환
@require_http_methods(["POST"])
def change(request):
    get_id = request.POST.get('id')
    try:
        todo = Todo.objects.get(id=get_id)
        # status 전환
        todo.status = 'WAIT' if todo.status == 'ING' else 'ING'
        todo.save()
    except Todo.DoesNotExist:
        print('전환할 Todo 가 없음...')

    return redirect('todo:list')

# Todo 완료 처리
@require_http_methods(["POST"]) # POST 요청으로만 받기
def success(request, id):

    try:
        todo = Todo.objects.get(id = id)
        todo.is_completed = True if todo.is_completed == False else False
        todo.save()
    except Todo.DoesNotExist:
        print('완료 처리할 Todo 없음...')

    return redirect('todo:list')

# Todo 삭제
@require_http_methods(["POST"])
def remove(request, id):
    try:
        todo = Todo.objects.get(id = id)
        todo.delete()
    except Todo.DoesNotExist:
        print("삭제할 Todo 없음...")

    return redirect('todo:list')
