import json
import os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from discovery import settings
from sparkjob.serializers import JobSerializer


@api_view(['POST'])
def create_entity(request):
    # data = JSONParser().parse(request)
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
    cmd = os.path.join(settings.SPARK_HOME, 'bin/spark-submit') \
          + " --master " + settings.SPARK_MASTER \
          + " --name " + name \
          + " " + job_py \
          + " '" + name \
          + "' 'file:" + path \
          + "' '" + schema + "'"
    os.system(cmd)
