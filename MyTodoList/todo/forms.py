from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content']
        widgets = {
            'title' : forms.TextInput(attrs={
                'autofoucs' : 'autofocus',
                'class' : 'form-control',
                'id' : 'title',
                'placeholder' : '할 일을 입력해주세요',
            }),
            'content' : forms.TextInput(attrs={
                'class' : 'form-control',
                'id' : 'content',
                'placeholder' : '세부 내용을 입력해주세요',
            }),
        }