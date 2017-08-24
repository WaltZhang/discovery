import os
import subprocess

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from discovery import settings
from sparkjob.models import JobModel
from sparkjob.serializers import JobSerializer


@api_view(['GET', 'POST'])
def entity_list(request):
    if request.method == 'GET':
        entities = JobModel.objects.all()
        serializer = JobSerializer(entities, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            name = serializer.data.get('name')
            path = serializer.data.get('path')
            schema = serializer.data.get('schema')
            create_job(os.path.join(settings.BASE_DIR, 'sparkjob/create_job.py'), name, path, schema)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    entities = JobModel.objects.all()
    serializer = JobSerializer(entities, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def entity_detail(request, id):
    try:
        entity = JobModel.objects.get(id=id)
    except JobModel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = JobSerializer(entity)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = JobSerializer(entity, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        entity.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
def create_entity(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        name = serializer.data.get('name')
        path = serializer.data.get('path')
        schema = serializer.data.get('schema')
        create_job(os.path.join(settings.BASE_DIR, 'sparkjob/create_job.py'), name, path, schema)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_job(job_py, name, path, schema):
    schema = schema.replace('\'', '\"')
    cmd = [os.path.join(settings.SPARK_HOME, 'bin/spark-submit'),
           '--master', settings.SPARK_MASTER,
           '--name', name,
           job_py, name,
           'file:' + path,
           '' + schema + '']
    subprocess.Popen(cmd)
    # with open('/tmp/' + name, mode='w') as tmp_output:
    #     subprocess.Popen(cmd, stdout=tmp_output, stderr=subprocess.STDOUT)
