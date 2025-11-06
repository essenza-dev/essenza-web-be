from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core'

    def ready(self):
        """
        Import authentication extensions when Django starts
        """
        try:
            import utils.docs  # This will register our JWTAuthenticationScheme
        except ImportError:
            pass