from django.shortcuts import render
from django.http import HttpResponseBadRequest
import django_tables2 as tables

from .forms import UploadForm
from .classifier import process_image
from . import models


# '/'
def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            upload = form.instance  # from .models import Uploads
            upload.classification = process_image(upload.file.path)
            upload.save(update_fields=['classification'])
            context = {"form" : upload}
            return render(request, 'process.html', context)
        return HttpResponseBadRequest()
    else:
        form = UploadForm()
        context = {"form" : form}
        return render(request, 'home.html', context)


class UploadTable(tables.Table):
    class Meta:
        model = models.Uploads
        template_name = 'django_tables2/bootstrap.html'
        attrs = {'class': 'paleblue'}


# '/admin_panel'
def admin_panel(request):
    table = UploadTable(models.Uploads.objects.all())
    tables.RequestConfig(request, paginate=True).configure(table)
    context = {"table" : table}
    return render(request, 'admin_panel.html', context)
