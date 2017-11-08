from django.conf.urls import url

from services import viewsets

app_name = 'services'
urlpatterns = [
    url(r'^api/$', viewsets.service_list),
    url(r'^api/(?P<name>\w{0,50})/$', viewsets.service_detail),
]
