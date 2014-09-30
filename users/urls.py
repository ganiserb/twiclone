# coding=utf-8
__author__ = 'gabriel'

from twiclone.settings import username_regex
from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^(?P<username>' + username_regex + r')/edit_tags_ajax/$', views.edit_tags_ajax, name='edit_tags_ajax'),
    url(r'^(?P<username>' + username_regex + r')/follow/$', views.follow_control, name='follow'),
    url(r'^(?P<username>' + username_regex + r')/post_profile_info/$', views.post_profile_info, name='post_profile_info'),
    url(r'^(?P<username>' + username_regex + r')/$', views.show_profile, name='show_profile'),

)