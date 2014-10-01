# coding=utf-8
__author__ = 'gabriel'

from twiclone.settings import username_regex
from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^post_new_tag_form/$', views.post_new_tag_form, name='post_new_tag_form'),
    url(r'^post_profile_form/$', views.post_profile_form, name='post_profile_form'),
    url(r'^post_edit_tags_form/$', views.post_edit_tags_form, name='post_edit_tags_form'),
    url(r'^(?P<username>' + username_regex + r')/follow/(?P<action>.+)/$',views.follow_control, name='follow'),  # action: 1 letter
#    url(r'^(?P<username>' + username_regex + r')/$', views.show_profile, name='show_profile'),

)