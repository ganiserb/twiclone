# coding=utf-8
__author__ = 'gabriel'

from django.conf.urls import patterns, url
from userprofile import views

urlpatterns = patterns('',
    #url(r'^(?P<username>.+)/edit/$', views.show_profile, name='edit'),  # TODO: Esta es la manera de hacerlo?
    url(r'^(?P<username>.+)/$', views.show_profile, name='show'),
)