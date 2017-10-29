from django.contrib import admin
from django.contrib.admin import ModelAdmin

from datainventory.models import InventoryModel


class InventoryModelAdmin(ModelAdmin):
    list_display = ['name', 'schema']
    class Meta:
        model = InventoryModel


admin.site.register(InventoryModel, InventoryModelAdmin)

