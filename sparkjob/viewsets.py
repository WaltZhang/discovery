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

            # create_job(os.path.join(settings.BASE_DIR, 'sparkjob/create_job.py'), name,
            #            os.path.join(settings.MEDIA_ROOT, file), schema)
            create_spark_job(name, os.path.join(settings.MEDIA_ROOT, file), schema)
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
    cmd = [create_py, '--master', settings.SPARK_MASTER, '--name', name]
    cmd.extend(args)
    with open('/tmp/' + name, mode='w') as tmp_output:
        proc_call(on_complete, name, tmp_output, cmd)


# def create_job(job_py, name, path, schema):
#     schema_str = json.dumps(schema)
#     cmd = [os.path.join(settings.SPARK_HOME, 'bin/spark-submit'),
#            '--master', settings.SPARK_MASTER,
#            '--name', name,
#            job_py, name,
#            'file:' + path,
#            '' + schema_str + '']
#     with open('/tmp/' + name, mode='w') as tmp_output:
#         proc_call(on_exit, name, tmp_output, cmd)


def proc_call(on_complete, file_name, tmp_out, *proc_args):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that
    would give to subprocess.Popen.
    """
    def run_in_thread(on_complete, file_name, tmp_out, proc_args):
        proc = subprocess.Popen(proc_args, stderr=subprocess.STDOUT, stdout=tmp_out)
        proc.wait()
        on_complete(file_name)
        return

    process = multiprocessing.Process(target=run_in_thread, args=(on_complete, file_name, tmp_out, *proc_args))
    process.start()
    # returns immediately after the thread starts
    return process


def on_complete(file):
    path = os.path.join('/tmp', file)
    with open(path, mode='r') as tmp_output:
        content = tmp_output.readlines()
    if '|count(1)|\n' in content:
        instance = JobModel.objects.get(name=file)
        instance.finalized = True
        instance.save()
        print(instance.id, instance.name, instance.finalized)
        os.remove(path)
    else:
        print(file, content)
