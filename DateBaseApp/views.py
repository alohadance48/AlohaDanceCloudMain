from django.contrib.messages import success
from django.shortcuts import render, redirect # Перенаправление и возврат шаблонов
from django.http import HttpResponseForbidden,HttpResponseBadRequest,HttpResponse # Возврат ошибок и статусов
from DateBaseApp.forms import LoginForm,RegisterForm,AdminForm,FormForSettings,UploadForm # Мои формы
from django.template.response import TemplateResponse # Возврат шаблонов
from DateBaseApp.models import User, LogForDeleteUsers,FileModel# Мои модели
from django.contrib import messages # Сообщения
from django.shortcuts import redirect, get_object_or_404
import bcrypt # Библиотека для шифрования данных
import os


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, FileModel  # Убедитесь, что вы импортируете необходимые модели
import os

def index(request):
    """
    Обрабатывает запрос на главную страницу.

    Проверяет, есть ли имя пользователя в сессии.
    Если пользователь аутентифицирован, отображает его данные.
    В противном случае перенаправляет на страницу входа.

    Args:
        request: Объект запроса.

    Returns:
        TemplateResponse или редирект на страницу входа.
    """
    print("Index view called")

    # Проверяем, есть ли имя пользователя в сессии
    username = request.session.get('username')
    if username:
        print('User is authenticated, processing request...')
        try:
            user = User.objects.get(name=username)
            email = user.email
            status = user.status
            all_files = FileModel.objects.all()

            if request.method == "POST" and 'delete_file' in request.POST:
                file_id = request.POST.get('file_id')
                try:
                    file_to_delete = FileModel.objects.get(id=file_id)
                    file_to_delete.delete()
                    os.remove(file_to_delete.file.path)  # Удаление файла из файловой системы
                    files = FileModel.objects.all().order_by('id')
                    for new_id, file in enumerate(files, start=1):
                        file.id = new_id
                        file.save()
                    messages.success(request, 'File deleted successfully.')
                except FileModel.DoesNotExist:
                    messages.error(request, 'File not found.')
                except Exception as e:
                    messages.error(request, f'Error deleting file: {str(e)}')

            elif request.method == "POST" and 'add_file' in request.POST:
                file_add = request.FILES['file']
                file = UploadForm(request.POST, request.FILES)
                if file.is_valid():
                    file.save()
                else:
                    return redirect('index')

            elif request.method == "GET" and 'donwload' in request.GET:
                file_name = request.GET.get('file_name')
                return file_install(request, file_name)


            # Создаем контекст для передачи в шаблон
            context = {
                'email': email,
                'status': status,
                'username': username,
                'files': all_files,
            }
            # Возвращаем ответ с шаблоном и контекстом
            return render(request, 'DateBaseApp/index.html', context)

        except User.DoesNotExist:
            print('User does not exist, redirecting to login...')
            messages.error(request, 'User does not exist.')
            return redirect('login')
    else:
        print('User is not authenticated, redirecting to login...')
        messages.error(request, 'You are not logged in.')
        return redirect('login')

    # Если ни одно из условий не выполнено, возвращаем редирект на страницу входа
    return redirect('login')


def file_install(request, file_id):
    # Получаем файл по ID, если файл не найден, будет возвращена 404 ошибка
    file = get_object_or_404(FileModel, id=file_id)

    # Открываем файл в бинарном режиме
    with open(file.file.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response[
            'Content-Disposition'] = f'attachment; filename="{file.file.name}"'  # Используем имя файла из поля file
        return response



def login(request):
    """Функция для аутентификации.
    Сравнивает данные из формы с данными из базы данных(sql.lite),
    если такие данные есть и эти данные введены корректно, то
     пользователь получает доступ ко всем ресурсам сайта,
     создается сессия для этого пользователя.
     Args:
        request, Form.Post : объекты запроса
        Returns:
            TemplateResponse(index) или redirect на страницу входа"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): # Проверка валидности формы
            """Если форма валидна - из формы извлекаются пароль,имя пользователя, email"""
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # Хеширование введенного пароля
            try:
                """Попытка получить данные о пользователе """
                user = User.objects.get(name=username)
                print(user.password) #debug
                print(hashed_password) # debug
                # Проверяем, соответствует ли введенный пароль хешированному паролю
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')) and user.email == email : #Сравнение паролей и email

                    messages.success(request, 'You are logged in') # Сообщение
                    request.session['username'] = username # Создание сессии
                    return redirect('index')  # redict на главную страницу
                else:
                    ip = request.META['REMOTE_ADDR']



                    """Если данные не совпадают, то возвращает на страницу авторизации,
                     это сделано для защиты от Bots"""
                    messages.error(request, 'Incorrect password') # Сообщение
                    return redirect('login') # Переброс на страницу авторизации

            except User.DoesNotExist:
                '''Обработка ошибок с данными БД'''
                messages.error(request, 'User does not exist')
                return redirect('login')
        else:
            """Обработка неправильной формы """
            messages.error(request, 'Please correct the errors in the form.')
            return redirect('login')
    else:
        """Если пользователь не отправил форму, то ему просто вернется наша страница с пустой формой """
        if request.session.get('username'):
            """Если у пользователя есть активная сессия, то она прекращается """
            request.session.flush()
        form = LoginForm() # форма
        context = {
            'login_form': form,
        }
        return TemplateResponse(request,'DateBaseApp/login.html', context, status=200) # Возврат



def register(request):
    """
    Обрабатывает запрос на регистрацию нового пользователя.

    Проверяет, есть ли имя пользователя в сессии.
    Если пользователь аутентифицирован и отправляет форму,
    проверяет ее на валидность и создает нового пользователя.

    Args:
        request: Объект запроса.

    Returns:
        Redirect на главную страницу или отображение формы регистрации.
    """
    if request.session.get('username'):
        print("Register view called")

        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')

                # Хешируем пароль
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                print(f"Creating user: {username}, email: {email}")

                try:
                    # Создаем нового пользователя
                    new_user = User.objects.create(name=username, email=email, password=hashed_password)
                    messages.success(request, 'Вы успешно зарегистрированы!')
                    return redirect('index')  # Перенаправление на главную страницу
                except Exception as e:
                    print(f"IntegrityError: {e}")
                    messages.error(request, 'Пользователь с таким email или именем уже существует.')
                    return render(request, 'DateBaseApp/Registr.html', {'form': form})

            else:
                print('Registration form is not valid.')
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
                return render(request, 'DateBaseApp/Registr.html', {'form': form})
        else:
            form = RegisterForm()

        return render(request, 'DateBaseApp/Registr.html', {'form': form})
    else:
        return redirect('login')


def admin_form(request):
    """
    Обрабатывает запросы на страницу администратора.

    Проверяет, есть ли имя пользователя в сессии.
    Если пользователь аутентифицирован, отображает форму
    или обрабатывает POST-запрос для удаления пользователя.

    Args:
        request: Объект запроса.

    Returns:
        TemplateResponse или редирект на главную страницу.
    """
    if request.session.get('username'):
        if request.method == 'GET':
            form = AdminForm()
            context = {'form': form}
            return TemplateResponse(request, 'DateBaseApp/admin.html', context, status=200)

        elif request.method == 'POST':
            form = AdminForm(request.POST)

            try:
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    email = form.cleaned_data.get('email')
                    password = form.cleaned_data.get('password')
                    comment = form.cleaned_data.get('comment')

                    # Получаем пользователя по имени
                    user = User.objects.get(name=username)

                    if user.status == 'root':
                        # Создаем запись в журнале и удаляем пользователя
                        logs = LogForDeleteUsers.objects.create(comment=comment)
                        user.delete()
                        print(True)
                        messages.success(request, 'Успешно!')
                        return redirect('index')
                    else:
                        return redirect('index')

            except User.DoesNotExist as e:
                print('User.DoesNotExist:', e)
                return redirect('index')

            except Exception as e:
                print('Error:', e)
                return TemplateResponse(request, 'Errors/ErrorRequests.html', status=500)

        else:
            return TemplateResponse(request, 'Errors/ErrorRequests.html', status=500)
    else:
        return redirect('login')




def root(request):
    if request.session.get('username'):
        user = User.objects.get(name=request.session.get('username'))
        if user.status == 'root':
            return TemplateResponse(request,'DateBaseApp/root.html')
        else:
            messages.success(request,'Error, do you have a root?')

            return redirect('index') and TemplateResponse(request,'DateBaseApp/root.html')
    else:
        return redirect('login')



