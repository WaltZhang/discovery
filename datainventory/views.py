from django.shortcuts import render, get_object_or_404

from datainventory.models import InventoryModel


def inventory_list(request):
    object_list = InventoryModel.objects.all()
    context = {
        'object_list': object_list
    }
    return render(request, 'datainventory/list.html', context=context)


def inventory_detail(request, id):
    instance = get_object_or_404(InventoryModel, id=id)
    record = read_data(instance.name)
    context = {
        'instance': instance,
        'record': record
    }
    return render(request, 'datainventory/detail.html', context)


def read_data(name):
    record = []
    with open('/tmp/' + name) as file:
        for line in file:
            record.append(line)
    return record
