from django.shortcuts import render
from django.http import HttpResponse


# This is where the request for '/' comes in
def home(request):
    return HttpResponse('hello world')