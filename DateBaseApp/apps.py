from django.apps import AppConfig


class DatebaseappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DateBaseApp'

    def ready(self):
        import DateBaseApp.signals
