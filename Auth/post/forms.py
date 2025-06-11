from .models import Post
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title' : forms.TextInput(attrs= {
                'class' : 'form-control',
                'placeholder' : '제목을 입력하세요'
            }),
            'content' : forms.Textarea(attrs= {
                'class' : 'form-control',
                'rows' : 5,
                'placeholder' : '내용을 입력하세요'
            }),
        }

    # title 필드에 대한 유효성 검사
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('제목을 입력해주세요.')
        return title

    # content 필드에 대한 유효성 검사
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('내용을 입력해주세요.')
        return content

    # 공통 유효성 검사
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if not title and not content:
            raise forms.ValidationError('제목과 내용을 모두 입력해주세요.')
        return cleaned_data