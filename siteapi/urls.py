# coding=utf-8
__author__ = 'gabriel'

from twiclone.settings import username_regex
from django.conf.urls import patterns, url
from siteapi import views

urlpatterns = patterns('',
    url(r'^profile/(?P<username>' + username_regex + r')/$',
        views.profile,
        name='profile'),
    url(r'^home/$',
        views.home,
        name='home'),
)