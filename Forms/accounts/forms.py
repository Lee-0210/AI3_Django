# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):  # UserCreationForm은 기본 유효성 검사 포함
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username'  : None,
            'email'     : None,
            'password1' : None,
            'password2' : None,
        }
        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control'}),
            # 'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
            # 'password1' : forms.PasswordInput(attrs={'class' : 'form-control'}),
            # 'password2' : forms.PasswordInput(attrs={'class' : 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['email', 'password1', 'password2']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})