# coding=utf-8
__author__ = 'gabriel'

from django.conf.urls import patterns, url
from twicles import views

urlpatterns = patterns('',
    url(r'^(?P<username>.+)/$', views.view_twicles, name='view'),
)