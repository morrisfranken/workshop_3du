from django.shortcuts import render
from django.http import HttpResponseBadRequest

from .forms import UploadForm


def process_image(img_path):
    print("img_path: ", img_path)
    return "cat"


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