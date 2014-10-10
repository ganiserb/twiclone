# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'twicles.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^register/$', 'users.views.register', name='register'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^u/', include('users.urls', namespace='users')),
    url(r'^t/', include('twicles.urls', namespace='twicles')),

    url(r'^api/', include('siteapi.urls', namespace='api')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
