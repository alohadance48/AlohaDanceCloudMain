# Django-projects

## Описание
Этот проект -  это облачное хранилище файлов
 
## Установка
1. Если вы на линуксе активируйте мой файл (venv.sh), после чего пропишите pip install -r requirements.txt
2. Если вы на винде, запустите мой файл (venv.bat), после чего пропишите pip install -r requirements.txt

## Использование
1. Зайдите в 'DateBaseApp/config.py' и выполните настройку backend 
2. Выполните миграции через 'python manage.py makemigrations' и 'python manage.py migrate'.
3. После установки перейдите в директорию с 'manage.py' и пропишите: "python manage.py runserver", после перейдите по ссылки 
которая появится в консоли.

## Дополнительные страницы:
1. AdminForm
2. NewUser
3. root

# Таблицы в SQL
1. DateBaseApp_user (Пользователи БД)
2. DateBaseApp_filemodel (Скаченные файлы в БД)
3. DateBaseApp_antibotslog (Система против D-dos)


# Стандарты 

## Шаблоны 
Возврат всех шаблонов осуществляется только через TemplateResponse. 

## Ошибки
Все ошибки возвращать через TemplateResponse + status = codeError

## Название и хранение шаблонов и статических файлов 
1. Страницы.html должны хранится в templates/DateBaseApp, ошибки.html в templates/Errors.
2. Страницы.css должны хранится в static/css, ошибки.css в static/Errors.
3. Страницы.js должны хранится в static/js, ошибки.js в static.js
4. Картинки.png должны хранится в static/png.

## База данных
1. Использовать только PSQL

## Формы
1. Всегда использовать {%csrf_token%}
2. В одном классе формы не более 4-х колонок ввода 

## Контакты
afonskiy.vlad@mail.ru 

## На данном этапе моя разработка идет на Gitlab, мой Github - зеркало.
