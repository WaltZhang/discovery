import csv
import uuid

import requests
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from fileconnector.forms import FileForm
from fileconnector.models import FileModel


def file_list(request):
    metadata = request.POST.get('metadata')
    file = request.POST.get('file')
    description = request.POST.get('description')
    create_data_set(request, metadata, file, description)
    queryset = FileModel.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'fileconnector/file_list.html', context)


def file_detail(request, id):
    instance = get_object_or_404(FileModel, id=id)
    meta_str, data = read_csv(instance.file.path)
    context = {
        'instance': instance,
        'meta_str': meta_str,
        'data': data
    }
    return render(request, 'fileconnector/file_detail.html', context)


def file_create(request):
    form = FileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # meta_str = read_file(instance.file.path)
        # meta = MetadataModel(description=instance.description,
        #                      file=instance.file,
        #                      metadata=meta_str)
        # meta.save()
        return redirect(reverse('files:detail', args=[instance.id]))
    context = {
        'form': form
    }
    return render(request, 'fileconnector/form.html', context)


def file_edit(request, id):
    instance = get_object_or_404(FileModel, id=id)
    form = FileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect(reverse('files:detail', args=[instance.id]))
    context = {
        'form': form
    }
    return render(request, 'fileconnector/form.html', context)


def create_data_set(request, metadata, file, description):
    data = {'name': str(uuid.uuid1()), 'schema': metadata, 'path': file, 'description': description}
    scheme = request.is_secure() and 'https' or 'http'
    domain = get_current_site(request)
    url = scheme + '://' + str(domain) + '/spark/create/'
    requests.post(url=url, json=data)


def read_csv(path):
    rows = []
    with open(path) as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        cols = [{title: 'StringType'} for title in header]
        for row in csv_file:
            rows.append(row)
        return cols, rows
