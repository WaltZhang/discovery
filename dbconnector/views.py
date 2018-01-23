from django.shortcuts import render

from dbconnector.models import ConnectionModel


def connector_list(request):
    object_list = ConnectionModel.objects.all()
    context = {
        'home_tab': '',
        'file_tab': '',
        'db_tab': 'active',
        'object_list': object_list,
    }
    return render(request, 'dbconnector/connector_list.html', context)


def connector_detail(request, id):
    pass