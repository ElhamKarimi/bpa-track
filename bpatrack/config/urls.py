# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # Django Admin, use {% url 'admin:index' %}
    # url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),
    # User management
    url(r'^users/', include("bpatrack.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# pattern for serving statically
urlpatterns += patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True})
)

urlpatterns += [
    url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
    url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permissin Denied")}),
    url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
    url(r'^500/$', default_views.server_error),
]
