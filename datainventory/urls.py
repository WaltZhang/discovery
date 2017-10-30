from django.conf.urls import url

from datainventory import views
from datainventory import viewsets

urlpatterns = [
    url(r'^$', views.inventory_list),
    url(r'^(?P<id>\d+)/$', views.inventory_detail),
    url(r'^api/$', viewsets.inventory_list),
    url(r'^api/(?P<id>\d+)/$', viewsets.inventory_detail)
]
