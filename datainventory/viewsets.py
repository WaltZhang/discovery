from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from datainventory.models import InventoryModel
from datainventory.serializers import InventorySerializer


@api_view(['GET', 'POST'])
def inventory_list(request):
    if request.method == 'GET':
        object_list = InventoryModel.objects.all()
        serializer = InventorySerializer(object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, id):
    try:
        instance = InventoryModel.objects.get(id=id)
    except InventoryModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = InventorySerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = InventorySerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
