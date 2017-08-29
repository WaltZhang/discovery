import csv, json, uuid, requests
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from fileconnector.forms import FileForm
from fileconnector.models import FileModel


def file_list(request):
    queryset = FileModel.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'fileconnector/file_list.html', context)


def file_detail(request, id):
    instance = get_object_or_404(FileModel, id=id)
    meta, data = read_csv(instance.file.path)
    context = {
        'instance': instance,
        'meta_str': meta,
        'uuid': uuid.uuid1().replace('-', '_'),
        'data': data
    }
    return render(request, 'fileconnector/file_detail.html', context)


def file_upload(request):
    form = FileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
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


def read_csv(path):
    rows = []
    with open(path) as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        cols = [{'name': title, 'type': 'string'} for title in header]
        for row in csv_file:
            rows.append(row)
        return cols, rows
