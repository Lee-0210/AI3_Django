from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib import messages

def home(request):
    return render(request, 'accounts/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 완료되었습니다!')
            return redirect('login')  # 로그인 페이지로 이동
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})
