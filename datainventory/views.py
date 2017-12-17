import json

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
    context = {
        'instance': instance,
        'sample': json.loads(instance.sample)
    }
    return render(request, 'datainventory/detail.html', context)
