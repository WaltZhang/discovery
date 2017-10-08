from django.conf.urls import url

from datainventory import viewsets

urlpatterns = [
    url(r'^api/$', viewsets.inventory_list),
    url(r'^api/(?P<id>\d+)/$', viewsets.inventory_detail)
]
