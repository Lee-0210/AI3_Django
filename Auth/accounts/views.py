from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from .forms import LoginForm, SignUpForm

# Create your views here.
# 회원가입
def signup(request):

  if request.method == 'POST':
    # UserCreationForm : Django에서 제공하는 회원가입 폼
    # form = UserCreationForm(request.POST)
    form = SignUpForm(request.POST)
    if form.is_valid():
      # 회원가입 성공
      form.save()
      return redirect('/')
  else:
    # 회원가입 실패 or 회원가입 화면
    # form = UserCreationForm()
    form = SignUpForm()

  return render(request, 'registration/signup.html', {'form': form})


# 로그인
def login_view(request):
  # 로그인 처리 요청
  if request.method == 'POST':
    # AuthenticationForm : Django에서 제공하는 로그인 폼
    # form = AuthenticationForm(request, data=request.POST)

    # LoginForm : 커스텀 로그인 폼
    form = LoginForm(request, data=request.POST)

    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      # 인증 처리 ➡ 성공 (User), 실패 (None)
      # authenticate() : DB 에 가입된 아이디, 비밀번호가 맞는지 확인
      user = authenticate(request, username=username, password=password)
      if user is not None:
        # 로그인 성공
        # login() : 세션에 사용자 정보를 저장
        login(request, user)
        return redirect('/')
      else:
        # 로그인 실패
        form.add_error(None, '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.')

  # 로그인 화면 or 로그인 실패
  else:
    # form = AuthenticationForm()
    form = LoginForm()

  return render(request, 'registration/login.html', {'form': form})


# 로그아웃
def logout_view(request):
  logout(request)
  return redirect('/')
