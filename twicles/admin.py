# coding=utf-8
from django.contrib import admin

from twicles.models import Twicle, UserSettings

# TODO: hacer que mis modelos se vean bien en el /admin

# Register your models here.
admin.site.register(Twicle)
admin.site.register(UserSettings)
