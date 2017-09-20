from django.shortcuts import render

from dbconnector.models import ConnectionModel


def connector_list(request):
    object_list = ConnectionModel.objects.all()
    context = {
        'object_list': object_list,
    }
    return render(request, 'dbconnector/connector_list.html', context)
