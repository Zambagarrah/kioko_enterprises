from django.apps import AppConfig
import core.signals

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

def ready(self):
