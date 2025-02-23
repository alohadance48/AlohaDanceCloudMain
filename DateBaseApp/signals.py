from django.db.models.signals import post_migrate
from django.dispatch import receiver
from DateBaseApp.models import User
from DateBaseApp.config import password
import bcrypt


@receiver(post_migrate)
def create_root_user(sender, **kwargs):
    if sender.name == 'DateBaseApp':  # Убедитесь, что имя приложения указано правильно
        # Создание пользователя root, если он не существует
        user, created = User.objects.get_or_create(
            name='root',  # Убедитесь, что это правильное поле для вашей модели
            defaults={
                'email': 'root@example.com',
                'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),  # Хэширование пароля
                'status': 'root',  # Убедитесь, что это правильное поле для вашей модели
            }
        )
        if created:
            print("Пользователь 'root' был создан.")
        else:
            print("Пользователь 'root' уже существует.")
