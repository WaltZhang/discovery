from django.conf.urls import url

from fileconnector import views
from fileconnector import viewsets


urlpatterns = [
    url(r'^$', views.file_list, name='list'),
    url(r'^create/$', views.file_create, name='create'),
    url(r'^(?P<id>\d+)/$', views.file_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', views.file_edit, name='edit'),
    url(r'^(?P<id>\d+)/delete/$', views.file_list, name='delete'),
    url(r'^api/$', viewsets.meta_list),
    url(r'^api/(?P<id>\d+)/$', viewsets.meta_detail),
]
