from django.conf.urls import url

from sparkjob.viewsets import entity_detail, csv_jobs, jdbc_jobs

urlpatterns = [
    url(r'^(?P<id>\d+)/$', entity_detail, name='detail'),
    url(r'^csv/$', csv_jobs, name='csv'),
    url(r'^jdbc/$', jdbc_jobs, name='jdbc'),
]
