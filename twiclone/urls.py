# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twiclone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

    url(r'^$', 'twicles.views.home', name='home'),   # TODO: Que si estoy logueado muestre mis twicles y los de quienes sigo
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^register/$', 'users.views.register', name='register'),


    url(r'^admin/', include(admin.site.urls)),

    url(r'^u/', include('users.urls', namespace='users')),   # QUESTION: Cómo hacer el include? "(r'^/',include ..." no funciona, include() solo tampoco
    url(r'^t/', include('twicles.urls', namespace='twicles')),




) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
