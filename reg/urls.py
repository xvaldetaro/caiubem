from django.conf.urls import patterns, url
from reg.views import FullCandidateFormView,SuccessView

urlpatterns = patterns('',
    url(r'^$', FullCandidateFormView.as_view(), name='new'),
    url(r'^success/$', SuccessView.as_view(), name='success'),
)

