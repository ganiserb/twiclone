# coding=utf-8
__author__ = 'gabriel'

from twiclone.settings import username_regex
from django.conf.urls import patterns, url
from twicles import views

urlpatterns = patterns('',
    url(r'^post/$', views.post_twicle, name='post_twicle'),
    url(r'^settings/post$', views.post_user_settings, name='post_user_settings'),
    url(r'^settings/$', views.show_user_settings, name='show_user_settings'),
)