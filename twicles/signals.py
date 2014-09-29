# coding=utf-8
__author__ = 'gabriel'

from django.db.models.signals import post_save
from django.dispatch import receiver
from twiclone.settings import AUTH_USER_MODEL

from twicles.models import UserSettings


@receiver(post_save, sender=AUTH_USER_MODEL)
def link_user_settings(instance, created, **kwargs):
    # Whenever a User is saved() this is executed
    if created:
        UserSettings.objects.get_or_create(user=instance)