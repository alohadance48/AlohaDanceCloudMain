from django import forms # Формы Django
from django.conf import settings # Настройки
from DateBaseApp.models import *

class LoginForm(forms.Form):
    """Форма авторизации """
    username = forms.CharField(max_length=20,label='Username:')
    email = forms.EmailField(label='Email:',max_length=30,min_length=10)
    password = forms.CharField(widget=forms.PasswordInput(),label="Password:",max_length=30,min_length=10)

class RegisterForm(forms.Form):
    """Форма для регистрации нового пользователя """
    username = forms.CharField(label='Username:', max_length=20,min_length=5)
    email = forms.EmailField(label='Email:',max_length=40,min_length=10,)
    password = forms.CharField(widget=forms.PasswordInput(),label="Password:",max_length=30,min_length=10)

class AdminForm(forms.Form):
    """Форма для удаления пользователей """
    username = forms.CharField(label='Username:',max_length=20,min_length=5)
    comment = forms.CharField(widget=forms.Textarea(),label="Comment:",max_length=1000,min_length=5)


class UploadForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['file']
