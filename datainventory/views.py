from datainventory.models import InventoryModel


def inventory_list():
    object_list = InventoryModel.objects.all()