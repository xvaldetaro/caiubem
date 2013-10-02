from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from home.views import HomeView
urlpatterns = patterns('',
    url(r'^/?$', HomeView.as_view()),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/', include('store.urls', namespace='store')),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
