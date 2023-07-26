from django.apps import AppConfig
class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

    def ready(self):
        from mainapp.utils.move_elevator import RunThread
        RunThread().start()

