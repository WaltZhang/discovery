from django.conf.urls import url

from sparkjob.viewsets import create_entity

urlpatterns = [
    url(r'^create/$', create_entity)
]
