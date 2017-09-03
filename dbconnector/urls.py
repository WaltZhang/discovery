from django.conf.urls import url

from dbconnector.viewsets import connector_detail, connector_list

urlpatterns = [
    url(r'^$', connector_list, name='list'),
    url(r'^(?P<id>\d+)/$', connector_detail, name='detail'),
]
