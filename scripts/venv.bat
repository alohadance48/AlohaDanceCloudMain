@echo off
set VENV_NAME=venv

:: Создание виртуальной среды
python -m venv %VENV_NAME%

:: Инструкция по активации
echo Для активации виртуальной среды выполните: %VENV_NAME%\Scripts\activate
