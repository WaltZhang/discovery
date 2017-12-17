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
    delimiter = request.GET.get('delimiter', ',')
    schema, data = read_csv(instance.file.path, delimiter)
    context = {
        'id': id,
        'instance': instance,
        'schema_str': json.dumps(schema),
        'uuid': str(uuid.uuid1()).replace('-', '_'),
        'data': json.dumps(data),
        'delimiter': delimiter
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


def read_csv(path, delimiter):
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter)
        header = next(reader)
        cols = [{title: 'string'} for title in header]
        rows = []
        for row in csv_file:
            rows.append(dict(zip(header, row.split(delimiter))))
        return cols, rows
