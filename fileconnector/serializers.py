from rest_framework import serializers

from fileconnector.models import MetadataModel


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataModel
        fields = [
            'id',
            'title',
            'file',
            'metadata'
        ]
