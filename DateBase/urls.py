"""
URL configuration for DateBase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # Админка
from django.urls import path ,re_path # Маршрутизация
from DateBaseApp.views import * # Представления

urlpatterns = [
    path('admin/', admin.site.urls), # Страница админа Django
    path('',login,name='login'), # Страница авторизации
    re_path(r'^index/$',index,name='index'), # Главная страница
    re_path(r'^NewUser/$',register, name='register'), # Страница регистрации нового пользователя
    re_path(r'^AdminForm/$',admin_form, name='admin_form'), # Моя страница админа(удаление пользователей)
    path('settings/', settings, name='setting'), # Система настройки моего backend

]
