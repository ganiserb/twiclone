# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twiclone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'twiclone.views.home', name='home'),   # TODO: Que si estoy logueado muestre mis twicles y los de quienes sigo
    url(r'^admin/', include(admin.site.urls)),

    url(r'^u/', include('userprofile.urls', namespace='userprofile')),
    url(r'^t/', include('twicler.urls', namespace='twicler')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # TODO: Hacer login


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
