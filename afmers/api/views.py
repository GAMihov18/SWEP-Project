from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from api.models import Account


# Create your views here.
def root(request):
    return HttpResponse(status=200)


def reports(request):
    match request.method:
        case "GET":
            return HttpResponse(status=404)
        case "POST":
            return HttpResponse(status=404)
