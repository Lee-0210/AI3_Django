from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import CustomUser

# UserCreationForm 상속받아 회원가입 폼 커스텀
class SignUpForm(UserCreationForm):
  class Meta:
    model = CustomUser  # CustomUser 모델을 사용
    fields = ['username', 'password1', 'password2', 'nickname', 'gender', 'age']

  def __init__(self, *args, **kwargs):
    super(SignUpForm, self).__init__(*args, **kwargs)
    # 필드 공통 설정
    for field in  self.fields.values():
      field.widget.attrs.update({'class': 'form-control'})
      
    # 개별 필드 설정
    self.fields['username'].widget.attrs.update({'placeholder': '아이디'})
    self.fields['password1'].widget.attrs.update({'placeholder': '비밀번호'})
    self.fields['password2'].widget.attrs.update({'placeholder': '비밀번호 확인'})
    self.fields['nickname'].widget.attrs.update({'placeholder': '닉네임'})
    self.fields['gender'].widget.attrs.update({'placeholder': '성별'})
    self.fields['age'].widget.attrs.update({'placeholder': '나이'})
    
    
# 커스텀 로그인 폼
class LoginForm(AuthenticationForm):
  class Meta:
    model = CustomUser  # CustomUser 모델을 사용
    fields = ['username', 'password']
  
  username = forms.CharField(
    label='아이디',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디'})
  )
  password = forms.CharField(
    label='비밀번호',
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'})
  )

  def __init__(self, *args, **kwargs):
    super(LoginForm, self).__init__(*args, **kwargs)
    # 필드 공통 설정
    for field in self.fields.values():
      field.widget.attrs.update({'class': 'form-control'})