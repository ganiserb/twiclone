# coding=utf-8
__author__ = 'gabriel'

from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^(?P<username>.+)/edit_tags_ajax/$', views.edit_tags_ajax, name='edit_tags_ajax'), # QUESTION: Si pongo esto al final no me lo encuentra o_O

    url(r'^(?P<username>.+)/follow/$', views.follow_control, name='follow'),

    url(r'^(?P<username>.+)/$', views.show_profile, name='show_profile'),
    url(r'^(?P<username>.+)/post_profile_info/$', views.post_profile_info, name='post_profile_info'),

)