# coding=utf-8
__author__ = 'gabriel'

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from userprofile.models import Profile


@receiver(post_save, sender=User)
def link_user_profile(instance, created, **kwargs):
    # Whenever a User is saved() this is executed
    if created:
        Profile.get_or_create(user=instance)    # TODO: Default avatar image
