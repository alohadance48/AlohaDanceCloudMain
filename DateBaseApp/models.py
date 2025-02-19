from django.db import models # Модели Django

class User(models.Model):
    """Основная модель для регистрации и авторизации """
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=4, default='user')

    def __str__(self):
        return self.name


class LogForDeleteUsers(models.Model):
    """Модель для логов рута """
    comment = models.CharField(max_length=128)
    delete_user = models.CharField(max_length=20)

    def __str__(self):
        return self.comment


