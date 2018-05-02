from django.apps import AppConfig

from . import settings


class DrfCachedTokenConfig(AppConfig):
    name = 'drf_cached_token'

    def ready(self):
        if settings.REGISTER_SIGNALS:
            from . import signals
