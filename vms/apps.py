from django.apps import AppConfig


class VmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vms'

    def ready(self) -> None:
        import vms.signals.handlers
