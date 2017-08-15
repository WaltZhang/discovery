from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fileconnector.models import MetadataModel
from fileconnector.serializers import MetadataSerializer


@api_view(['GET', 'POST'])
def meta_list(request):
    if request.method == 'GET':
        object_list = MetadataModel.objects.all()
        serializer = MetadataSerializer(object_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MetadataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def meta_detail(request, id):
    try:
        metadata = MetadataModel.objects.get(id=id)
    except MetadataModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MetadataSerializer(metadata)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MetadataSerializer(metadata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        metadata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
