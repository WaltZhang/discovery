import json
import multiprocessing
import os
import subprocess

from rest_framework import status
from rest_framework.decorators import api_view
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
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            name = serializer.data.get('name')
            schema = serializer.data.get('schema')
            file = serializer.data.get('file')

            create_job(os.path.join(settings.BASE_DIR, 'sparkjob/create_job.py'), name,
                       os.path.join(settings.MEDIA_ROOT, file), schema)
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
        serializer = JobSerializer(entity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        entity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def create_job(job_py, name, path, schema):
    schema_str = json.dumps(schema)
    # schema_str = schema_str.replace('\'', '\\\\\"')
    cmd = [os.path.join(settings.SPARK_HOME, 'bin/spark-submit'),
           '--master', settings.SPARK_MASTER,
           '--name', name,
           job_py, name,
           'file:' + path,
           '' + schema_str + '']
    # popenAndCall(on_exit, cmd)
    with open('/tmp/' + name, mode='w') as tmp_output:
        popenAndCall(on_exit, tmp_output, cmd)


def popenAndCall(onExit, tmp_out, *popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that
    would give to subprocess.Popen.
    """

    def runInThread(onExit, tmp_out, popenArgs):
        proc = subprocess.Popen(popenArgs, stderr=subprocess.STDOUT, stdout=tmp_out)
        proc.wait()
        onExit(tmp_out)
        return

    process = multiprocessing.Process(target=runInThread, args=(onExit, tmp_out, *popenArgs))
    process.start()
    # returns immediately after the thread starts
    return process


def on_exit(file):
    with open('/tmp/' + file, mode='r') as tmp_output:
        content = tmp_output.readlines()
    if file in content:
        instance = JobModel.objects.get(name=file)
        print(instance)
        instance.embryonic = False
        instance.save()
    else:
        print(file, content)
