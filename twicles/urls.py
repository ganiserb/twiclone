# coding=utf-8
__author__ = 'gabriel'

from twiclone.settings import username_regex
from django.conf.urls import patterns, url
from twicles import views

urlpatterns = patterns('',
    url(r'^post/$', views.post_twicle, name='post_twicle'),
    url(r'^(?P<username>' + username_regex + r')/$', views.view_twicles, name='view'),

)