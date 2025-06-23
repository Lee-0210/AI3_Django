from django.shortcuts import render
from .models import Todo
from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    return render(request, 'index.html')

def list(request):
    list = Todo.objects.all()
    return render(request, 'list.html', {"list" : list})

@require_http_methods(["POST"])
def success(request):
    get_id = request.POST.get('id')
    todo = Todo.objects.get(id = get_id)
    print(f"조회한 todo : {todo}")