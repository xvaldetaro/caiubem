from django.conf.urls import patterns, url
from home.views import HomeView,AboutView,ContactView,RegView

urlpatterns = patterns('',
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^reg/$', RegView.as_view(), name='reg'),
)