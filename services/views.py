from django.shortcuts import render

from services.models import ServiceModel


def service_list(request):
    object_list = ServiceModel.objects.all()
    context = {
        'object_list': object_list
    }
