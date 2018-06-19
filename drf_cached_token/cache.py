from django.core.cache import caches

from . import settings


def get_cache():
    return caches[settings.BACKEND]


def get_cache_key(key):
    return 'drf_cached_token:{key}'.format(key=key)


def clear_cache():
    cache = get_cache()
    cache.delete_pattern('drf_cached_token*')
