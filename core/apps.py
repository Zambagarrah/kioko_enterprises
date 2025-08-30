from django.apps import AppConfig

def ready(self):
    import core.signals


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
