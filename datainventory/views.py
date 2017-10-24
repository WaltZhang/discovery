from django.shortcuts import render

from datainventory.models import InventoryModel


def inventory_list(request):
    object_list = InventoryModel.objects.all()
    context = {
        'object_list': object_list
    }
    return render(request, 'datainventory/list.html', context=context)
