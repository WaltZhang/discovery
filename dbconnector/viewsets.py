from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dbconnector import serializers
from dbconnector.models import ConnectionModel


@api_view(['GET', 'POST'])
def connector_list(request):
    if request.method == 'GET':
        object_list = ConnectionModel.objects.all()
        serializer = serializers.ConnectionSerializer(object_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.ConnectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def connector_detail(request, id):
    try:
        instance = ConnectionModel.objects.get(id=id)
    except ConnectionModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = serializers.ConnectionSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = serializers.ConnectionSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
