import os
import multiprocessing
import subprocess
import uuid

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
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            name = str(uuid.uuid1())
            name = name.replace('-', '_')
            description = serializer.data.get('description')
            metadata = serializer.data.get('metadata')
            file = serializer.data.get('file')
            schema = {'name': name, 'schema': metadata, 'description': description}

            create_job(os.path.join(settings.BASE_DIR, 'sparkjob/create_job.py'), name, os.path.join(settings.MEDIA_ROOT, file), schema)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def entity_detail(request, id):
    try:
        entity = JobModel.objects.get(id=id)
    except JobModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = JobSerializer(entity)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = JobSerializer(entity, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        entity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def create_job(job_py, name, path, schema):
    schema = schema.replace('\'', '\"')
    cmd = [os.path.join(settings.SPARK_HOME, 'bin/spark-submit'),
           '--master', settings.SPARK_MASTER,
           '--name', name,
           job_py, name,
           'file:' + path,
           '' + schema + '']
    popenAndCall(on_exit, cmd)
    # with open('/tmp/' + name, mode='w') as tmp_output:
    #     subprocess.Popen(cmd, stdout=tmp_output, stderr=subprocess.STDOUT)



def popenAndCall(onExit, *popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that
    would give to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs):
        proc = subprocess.Popen(popenArgs)
        proc.wait()
        onExit()
        return
    process = multiprocessing.Process(target=runInThread, args=(onExit, *popenArgs))
    process.start()
    # returns immediately after the thread starts
    return process


def on_exit():
    print("On Exit...")
