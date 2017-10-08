from rest_framework import serializers

from sparkjob.models import CsvModel, JdbcModel


class CsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvModel
        fields = '__all__'


class JdbcSerializer(serializers.ModelSerializer):
    class Meta:
        model = JdbcModel
        fields = '__all__'
