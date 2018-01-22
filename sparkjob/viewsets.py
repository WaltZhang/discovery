import multiprocessing
import os
import subprocess

from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from discovery import settings
from sparkjob.models import CsvModel, JdbcModel
from sparkjob.serializers import CsvSerializer, JdbcSerializer


@api_view(['GET', 'POST'])
def csv_jobs(request):
    if request.method == 'GET':
        entities = CsvModel.objects.all()
        serializer = CsvSerializer(entities, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CsvSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            name = serializer.data.get('name')
            schema = serializer.data.get('schema')
            csv_file = serializer.data.get('file')
            delimiter = serializer.data.get('delimiter')

            create_spark_job(name, 'csv', 'file://' + os.path.join(settings.MEDIA_ROOT, csv_file), schema, name, delimiter)
            return redirect(reverse('inventory:data_list'))
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def jdbc_jobs(request):
    if request.method == 'GET':
        entities = JdbcModel.objects.all()
        serializer = JdbcSerializer(entities, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = JdbcSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            name = serializer.data.get('name')
            connector = serializer.data.get('connector')
            table = serializer.data.get('table')

            create_spark_job(name, 'jdbc', os.path.join(settings.MEDIA_ROOT, table), connector)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def entity_detail(request, id):
    try:
        entity = CsvModel.objects.get(id=id)
    except CsvModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CsvSerializer(entity)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CsvSerializer(entity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        delete_job(os.path.join(settings.BASE_DIR, 'sparkjob/delete_job.py'), entity.name)
        entity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def delete_job(job_py, name):
    cmd = [os.path.join(settings.SPARK_HOME, 'bin/spark-submit'),
           '--master', settings.SPARK_MASTER,
           '--name', name,
           job_py, name]
    subprocess.Popen(cmd)


def create_spark_job(name, *args):
    create_py = os.path.join(settings.BASE_DIR, 'sparkjob/create_job.py')
    cmd = [os.path.join(settings.SPARK_HOME, 'bin/spark-submit'),
           '--master', settings.SPARK_MASTER, '--name', name, create_py]
    cmd.extend(args)
    proc_call(create_inventory, name, cmd)


def proc_call(on_complete, file_name, *proc_args):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that
    would give to subprocess.Popen.
    """
    def run_in_thread(on_complete, file_name, proc_args):
        proc = subprocess.Popen(proc_args)
        proc.wait()
        on_complete(file_name)
        return

    process = multiprocessing.Process(target=run_in_thread, args=(on_complete, file_name, *proc_args))
    process.start()
    # returns immediately after the thread starts
    return process


def create_inventory(name):
    query_py = os.path.join(settings.BASE_DIR, 'sparkjob/create_inventory.py')
    cmd = [os.path.join(settings.SPARK_HOME, 'bin/spark-submit'),
           '--master', settings.SPARK_MASTER,
           '--name', name,
           query_py, name]
    subprocess.Popen(cmd)
