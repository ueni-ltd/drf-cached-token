from rest_framework.authentication import TokenAuthentication

from .cache import get_cache
from .cache import get_cache_key
from . import settings


class QueryParamsTokenAuthenticationMixin:

    def authenticate(self, request):
        token = request.query_params.get(settings.TOKEN_QUERY_PARAM)
        if token:
            return self.authenticate_credentials(token)

        return super().authenticate(request)


class QueryParamsTokenAuthentication(QueryParamsTokenAuthenticationMixin, TokenAuthentication):
    pass


class CachedTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        cache = get_cache()
        cache_key = get_cache_key(key)
        token = cache.get(cache_key)
        if token is None:
            user, token = super().authenticate_credentials(key)
            cache.set(cache_key, token, timeout=settings.TIMEOUT)
            return user, token

        return token.user, token


class CachedQueryParamsTokenAuthentication(QueryParamsTokenAuthenticationMixin, CachedTokenAuthentication):
    pass
