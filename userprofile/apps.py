# coding=utf-8
__author__ = 'gabriel'
from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    name = "userprofile"
    vervose_name = "User profile"

    def ready(self):
        from userprofile import signals