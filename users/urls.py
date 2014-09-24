# coding=utf-8
__author__ = 'gabriel'

from django.conf.urls import patterns, url
from userprofile import views

urlpatterns = patterns('',
    url(r'^(?P<username>.+)/$', views.view_profile, name='view'),
    url(r'^(?P<username>.+)/edit_tags_ajax/$', views.edit_tags_ajax, name='edit_tags_ajax'),
)