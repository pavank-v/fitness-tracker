from django.apps import AppConfig


class MyfitappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myfitapp'

    def ready(self) -> None:
        import myfitapp.signals