# coding=utf-8
__author__ = 'gabriel'
from django.apps import AppConfig


class TwiclesConfig(AppConfig):
    name = "twicles"
    vervose_name = "Twicles"

    def ready(self):
        from twicles import signals