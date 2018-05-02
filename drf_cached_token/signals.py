from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_delete

from rest_framework.authtoken.models import Token

from .cache import get_cache
from .cache import get_cache_key

user_model = get_user_model()


def user_change_handler(sender, instance, *args, **kwargs):
    try:
        token = instance.auth_token
    except Token.DoesNotExist:
        return

    token.user = instance
    cache = get_cache()
    cache.set(get_cache_key(token.key), token)


@receiver(post_save, sender=user_model)
def user_update_handler(sender, instance, *args, **kwargs):
    user_change_handler(sender, instance, *args, **kwargs)


@receiver(m2m_changed, sender=user_model.groups.through)
def user_groups_handler(sender, instance, *args, **kwargs):
    user_change_handler(sender, instance, *args, **kwargs)


@receiver(m2m_changed, sender=user_model.user_permissions.through)
def user_permissions_handler(sender, instance, *args, **kwargs):
    user_change_handler(sender, instance, *args, **kwargs)


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def user_delete_handler(sender, instance, *args, **kwargs):
    try:
        token = instance.auth_token
    except Token.DoesNotExist:
        return

    token.user = instance
    cache = get_cache()
    cache.delete(get_cache_key(token.key))


@receiver(post_save, sender=Token)
def token_update_handler(sender, instance, *args, **kwargs):
    instance.user = instance.user  # Make sure the user data is fetched
    cache = get_cache()
    cache.set(get_cache_key(instance.key), instance)


@receiver(post_delete, sender=Token)
def token_delete_handler(sender, instance, *args, **kwargs):
    cache = get_cache()
    cache.delete(get_cache_key(instance.key))
