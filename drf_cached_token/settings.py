from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SETTINGS = getattr(settings, 'DRF_CACHED_TOKEN', {})

TIMEOUT = SETTINGS.get('TIMEOUT', None)
BACKEND = SETTINGS.get('BACKEND', 'default')

if not hasattr(settings, 'CACHES') or BACKEND not in settings.CACHES:
    raise ImproperlyConfigured('BACKEND must be one of django caches specified in your settings.py')

REGISTER_SIGNALS = SETTINGS.get('REGISTER_SIGNALS', True)
TOKEN_QUERY_PARAM = SETTINGS.get('TOKEN_QUERY_PARAM', 'api_token')
