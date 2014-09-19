# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twiclo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'twiclo.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^u/', include('userprofile.urls', namespace='userprofile')),
    url(r'^t/', include('twicler.urls', namespace='twicler')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
