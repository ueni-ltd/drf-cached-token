# drf-cached-token

Django app that that implements a cached version of `rest_framework` token authentication.

Installation
============

* Install using pip:

    ```bash
    pip install -e git+https://github.com/ueni-ltd/drf-cached-token.git@v0.1.0#egg=drf_cached_token
    ```

* Add ``drf_cached_token`` to ``INSTALLED_APPS`` in ``settings.py``:

    ```python
    INSTALLED_APPS = (
        ...
        'drf_cached_token',
        ...
    )
    ```

* Configure the app in ``settings.py``, bellow are shown the default settings:

    ```python
    DRF_CACHED_TOKEN = {
        'TIMEOUT': None,
        'BACKEND': 'default',
        'REGISTER_SIGNALS': True,
        'TOKEN_QUERY_PARAM': 'api_token',
    }
    ```

    * `TIMEOUT` - timeout for keys in the cache specified in seconds.

    * `BACKEND` - name of the django cache used to store the tokens.    

    * `REGISTER_SIGNALS` - boolean indicating wheter the app should register signals that update the cache
when the token or user objects are updated, created or deleted.

    * `TOKEN_QUERY_PARAM` - name of the query parameter from which the token will be taken, when using
`QueryParamsTokenAuthentication`.

Usage
=====
* You can set it as default in your `rest_framework` settings:

    ```python
    REST_FRAMEWORK = {
        ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'drf_cached_token.authentication.CachedTokenAuthentication',
        ),
        ...
    }
    ```

* Or just use it in your view:
    ```python
    from rest_framework.viewsets import ModelViewSet
    from drf_cached_token.authentication import CachedTokenAuthentication


    class MyVieSet(ModelViewSet):
        authentication_classes = (CachedTokenAuthentication,)
        ...
    ```
