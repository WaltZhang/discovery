from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from services.models import ServiceModel
from services.serializers import ServiceSerializer


@api_view(['GET', 'POST'])
def service_list(request):
    if request.method == 'GET':
        object_list = ServiceModel.objects.all()
        serializer = ServiceSerializer(object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request, name):
    try:
        instance = ServiceModel.objects.get(name=name)
    except ServiceModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceSerializer(instance=instance)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ServiceSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
