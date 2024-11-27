from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from front_end.forms import AccountCreationForm

# Create your views here.


def home(request):
    return render(request, "base.html")


def register(request):
    form = AccountCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/")
    else:
        form = AccountCreationForm()
    return render(request, "Register.html", {"form": form})


login = LoginView.as_view(template_name="Login.html")
