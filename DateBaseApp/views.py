from django.shortcuts import render, redirect # Перенаправление и возврат шаблонов
from django.http import HttpResponseForbidden,HttpResponseBadRequest,HttpResponse # Возврат ошибок и статусов
from DateBaseApp.forms import LoginForm,FileInstall,FilesDispatch,RegisterForm,AdminForm,FormForSettings # Мои формы
from django.template.response import TemplateResponse # Возврат шаблонов
from DateBaseApp.models import User, LogForDeleteUsers # Мои модели
from django.contrib import messages # Сообщения
from django.conf import settings # Настройки Django
import bcrypt # Библиотека для шифрования данных



# Create your views here.
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
    if request.session.get('username'):
        username = request.session.get('username')

        if username:
            print('User is authenticated, redirecting...')
            user = User.objects.get(name=username)
            email = user.email
            status = user.status

            # Создаем контекст для передачи в шаблон
            context = {
                'email': email,
                'status': status,
                'username': username,
            }

            # Возвращаем ответ с шаблоном и контекстом
            return TemplateResponse(request, 'DateBaseApp/index.html', context, status=200)
        else:
            print('No username found in session, redirecting to login...')
            return redirect('login')
    else:
        print('User is not authenticated, redirecting to login...')
        messages.error(request, 'You are not logged in')
        return redirect('login')


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
                return TemplateResponse(request, 'Errors/ErrorRequests.html', status=502)

        else:
            return TemplateResponse(request, 'Errors/ErrorRequests.html', status=502)
    else:
        return redirect('login')


def settings(request):
    """
    Обрабатывает запросы на страницу настроек.

    Проверяет, включены ли настройки.
    Если настройки включены и метод запроса POST,
    обрабатывает форму для создания нового пользователя.

    Args:
        request: Объект запроса.

    Returns:
        HttpResponse с сообщением об успешной настройке или
        TemplateResponse с формой настроек.
    """
    if settings.START_SETTING:
        if request.method == 'POST':
            form = FormForSettings(request.POST)

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                email = form.cleaned_data.get('email')

                # Хешируем пароль
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                # Создаем нового пользователя
                User.objects.create(username=username, password=hashed_password, email=email, status='root')

                return HttpResponse('<h1>Настройка завершена, пожалуйста, перезапустите проект с START_SETTING=False</h1>')
        else:
            form = FormForSettings()
            context = {'form': form}
            return TemplateResponse(request, 'DateBaseApp/setting.html', context, status=200)
    else:
        return redirect('login')

