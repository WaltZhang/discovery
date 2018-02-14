from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.RegisterView.as_view(), name='register'),
]
