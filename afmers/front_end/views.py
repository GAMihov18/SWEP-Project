from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def Home(request):
    return render(request, "base.html")


def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "Register.html", {"form": form})
