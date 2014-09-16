# coding=utf-8
__author__ = 'gabriel'

from django.conf.urls import patterns, url
from userprofile import views

urlpatterns = patterns('',
    url(r'^(?P<username>.+)/edit/$', views.edit_profile, name='edit'),
    url(r'^(?P<username>.+)/$', views.show_profile, name='show'),
)