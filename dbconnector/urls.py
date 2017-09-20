from django.conf.urls import url

from dbconnector import views
from dbconnector import viewsets

urlpatterns = [
    url(r'^$', views.connector_list, name='list'),
    url(r'^api/$', viewsets.connector_list),
    url(r'^api/(?P<id>\d+)/$', viewsets.connector_detail),
]
