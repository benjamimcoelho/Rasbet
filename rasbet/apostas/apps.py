from django.apps import AppConfig


class ApostasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apostas'
    def ready(self):
            from apostas.scheduler import scheduler
            scheduler.start()

        