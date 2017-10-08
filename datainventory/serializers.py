from rest_framework import serializers

from datainventory import models


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InventoryModel
        fields = '__all__'
