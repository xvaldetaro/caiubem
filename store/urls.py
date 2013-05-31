from django.conf.urls import patterns, url
from store.views import ProductView,ProductListView

urlpatterns = patterns('',
    url(r'^product/(?P<pk>\d+)/$', ProductView.as_view(), name='product'),
    url(r'^product_list/$', ProductListView.as_view(), name='product_list'),
)