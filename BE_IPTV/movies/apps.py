from django.apps import AppConfig
from django.conf import settings

class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    def ready(self):
        from . import scheduler
        scheduler.start()
