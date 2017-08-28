from django.conf.urls import url

from sparkjob.viewsets import entity_list, entity_detail

urlpatterns = [
    url(r'^$', entity_list, name='list'),
    url(r'^(?P<id>\d+)/$', entity_detail, name='detail'),
]
