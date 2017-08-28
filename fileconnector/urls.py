from django.conf.urls import url

from fileconnector import views


urlpatterns = [
    url(r'^$', views.file_list, name='list'),
    url(r'^upload/$', views.file_upload, name='upload'),
    url(r'^(?P<id>\d+)/$', views.file_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', views.file_edit, name='edit'),
    url(r'^(?P<id>\d+)/delete/$', views.file_list, name='delete'),
]
