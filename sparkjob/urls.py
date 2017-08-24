from django.conf.urls import url

from sparkjob.viewsets import create_entity, entity_list, entity_detail

urlpatterns = [
    url(r'^$', entity_list),
    url(r'^(?P<id>\d+)/$', entity_detail),
]
