#!/bin/bash

VENV_NAME="venv"

# Создание виртуальной среды
python3 -m venv myenv
source myenv/bin/activate

# Инструкция по активации
echo "Виртуальная среда созданная, теперь можно запускать мои программы!"
