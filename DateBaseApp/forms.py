from django import forms # Формы Django
from django.conf import settings # Настройки

class LoginForm(forms.Form):
    """Форма авторизации """
    username = forms.CharField(max_length=20,label='Username:')
    email = forms.EmailField(label='Email:',max_length=30,min_length=10)
    password = forms.CharField(widget=forms.PasswordInput(),label="Password:",max_length=30,min_length=10)


class EmailForm(forms.Form):
    """ Отображение email """
    email = forms.EmailField(label='Email:',max_length=30,min_length=10)

class UserName(forms.ModelForm):
    """Отображения username"""
    username = forms.CharField(max_length=20,min_length=4,label='Usernmae:')

class StatusForm(forms.ModelForm):
    """Отображение статуса """
    status = forms.CharField(min_length=4,max_length=4,label='Status:')

class FilesDispatch(forms.Form):
    """Форма для отправки файлов """
    file = forms.FileField(label='Select a file:')

class FileInstall(forms.Form):
    """Файл для установки файлов """
    file = forms.FilePathField(label='Select a file for installation:',path=settings.FILES_FOR_DB,allow_files=True,allow_folders=True)

class RegisterForm(forms.Form):
    """Форма для регистрации нового пользователя """
    username = forms.CharField(label='Username:', max_length=20,min_length=5)
    email = forms.EmailField(label='Email:',max_length=40,min_length=10,)
    password = forms.CharField(widget=forms.PasswordInput(),label="Password:",max_length=30,min_length=10)

class AdminForm(forms.Form):
    """Форма для удаления пользователей """
    username = forms.CharField(label='Username:',max_length=20,min_length=5)
    comment = forms.CharField(widget=forms.Textarea(),label="Comment:",max_length=1000,min_length=5)

class FormForSettings(forms.Form):
    """Форма для настроек """
    username = forms.CharField(label='Username:', max_length=20,min_length=5)
    email = forms.EmailField(label='Email:',max_length=40,min_length=10,)
    password = forms.CharField(widget=forms.PasswordInput(),label="Password:",max_length=30,min_length=10)



