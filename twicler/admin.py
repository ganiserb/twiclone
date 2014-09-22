# coding=utf-8
from django.contrib import admin

from twicler.models import Twiclo, UserSettings

# TODO: hacer que mis modelos se vean bien en el /admin

# Register your models here.
admin.site.register(Twiclo)
admin.site.register(UserSettings)
