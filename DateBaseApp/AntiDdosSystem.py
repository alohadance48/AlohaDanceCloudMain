from DateBaseApp.models import AntiBotsLog
from DateBaseApp.config import quantity_requests
from django.conf import settings
from datetime import datetime
import asyncio
import os
import json

class AntiDDosSystem:
    """
    Класс для реализации системы защиты от DDoS-атак.

    Атрибуты:
        ip (str): IP-адрес, который отслеживается.
        counter (int): Счетчик запросов.
        time (bool): Флаг, указывающий, истекло ли время.
        start_mode (bool): Флаг, указывающий, активирован ли режим защиты.
        name_file (str): Имя файла для сохранения логов.
    """

    def __init__(self) -> None:
        """Инициализация атрибутов класса."""
        self.ip = ''
        self.counter = 0
        self.time = False
        self.start_mode = False
        self.name_file = ''
        self.all_ip = []

    def set_value(self, value: str) -> None:
        """
        Устанавливает IP-адрес.

        Аргументы:
            value (str): IP-адрес для установки.
        """
        self.ip = value
        self.all_ip.append(value)

    def add_all_user_ip(self,ip_user):
        anti_bot = AntiBotsLog.objects.get(IP=ip_user)
        trying = anti_bot.trying
        trying += 1
        if anti_bot.ip:
            add_try = AntiBotsLog.objects.update(trying=trying)

        else :
            new_user_ip = AntiBotsLog.objects.create(IP=ip_user, trying=trying)

    def blocked_ip_user(self):
        user_ip = AntiBotsLog.objects.get(IP=self.ip)
        if user_ip.trying >= 3:
            pass
        else :
            pass



    def add_bot(self, bot_ip: str) -> None:
        """
        Добавляет IP-адрес бота в лог.

        Аргументы:
            bot_ip (str): IP-адрес бота.
        """
        AntiBotsLog.objects.get_or_create(IP=self.ip)

    async def timer(self) -> None:
        """
        Запускает таймер на 60 секунд и сбрасывает счетчик запросов.
        Устанавливает флаг времени в True после истечения таймера.
        """
        self.counter = 0
        await asyncio.sleep(60)
        self.time = True
        self.name_file = 'log' + datetime.now().strftime('%y%m%d%H%M%S')

    async def counter_requests(self, requests: bool) -> None:
        """
        Увеличивает счетчик запросов, если запрос был получен.

        Аргументы:
            requests (bool): Флаг, указывающий, был ли получен запрос.
        """
        if requests:
            self.counter += 1


    async def start_spare_mode(self) -> None:
        """
        Проверяет, активирован ли режим защиты, и устанавливает флаг start_mode в True,
        если время истекло и счетчик запросов достиг заданного количества.
        """
        if self.time and self.counter == quantity_requests:
            self.start_mode = True

    async def logs(self) -> None:
        """
        Сохраняет логи запросов в файл в формате JSON.
        Логи содержат количество запросов, IP-адрес и дату.
        """
        dir = os.path.join(settings.BASE_DIR, 'logs')
        os.makedirs(dir, exist_ok=True)  # Создает директорию, если она не существует
        os.chdir(dir)

        # Получение текущей даты и времени
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.date = {
            'Запросов в минуту:': self.counter,
            'IP:': self.all_ip,
            'Date:': current_date
        }

        with open(self.name_file, 'w', encoding='utf-8') as file:
            json.dump(self.date, file, ensure_ascii=False, indent=4)
            print('Логи сохранены')
