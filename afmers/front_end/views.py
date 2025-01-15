from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from front_end.forms import AccountCreationForm, ReportForm, TaskForm, UpdateTaskForm
from api.controllers import *
from api.models import Report, Task

# Create your views here.


def home(request):
    reports = Report.objects.all()[::-1][:5]
    return render(request, "Home.html", {"reports": reports})


def register(request):
    form = AccountCreationForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.is_superuser = False
        account.is_staff = False
        account.is_active = True
        account.is_deleted = False
        account.save()
        return redirect("/login")
    else:
        print(form.errors)
        # form = AccountCreationForm()
    return render(request, "Register.html", {"form": form})


login = LoginView.as_view(template_name="Login.html")


def map(request):
    return render(request, "map.html")


def reports(request):
    context = {"reports": ReportController.all()[::-1]}
    return render(request, "reports_main.html", context=context)


def create_report(request):
    form = ReportForm(request.POST)
    if form.is_valid():
        report = form.save(commit=False)
        report.account = request.user
        report.save()
        return redirect("/")
    else:
        form = ReportForm()
    return render(request, "Create_Report.html", {"form": form})


def create_task(request, pk):
    request.method = "POST"
    report = get_object_or_404(Report, pk=pk)
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.report = report
        task.save()
        return redirect("/reports")
    else:
        form = TaskForm()
    return render(request, "Create_Task.html", {"form": form})


def tasks(request, pk):
    report = get_object_or_404(Report, pk=pk)
    tasks = Task.objects.filter(report=report)
    return render(request, 'Tasks_main.html', {"tasks": tasks})

def assigned_tasks(request, pk):
    tasks = Task.objects.filter(username=pk)
    return render(request, 'Tasks_main.html', {"tasks": tasks})

def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    request.method = 'POST'
    form = UpdateTaskForm(request.POST, instance=task)
    if form.is_valid():
        task.save()
        return redirect('/')
    else:
        form = UpdateTaskForm(instance=task)
    return render(request, 'Create_Task.html', {'form': form})


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    request.method = 'POST'
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        task.save()
        return redirect('/')
    else:
        form = TaskForm(instance=task)
    return render(request, 'Create_Task.html', {'form': form})


def update_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    request.method = 'POST'
    form = ReportForm(request.POST, instance=report)
    if form.is_valid():
        report.save()
        return redirect('/')
    else:
        form = ReportForm(instance=report)
    return render(request, 'Create_Report.html', {'form': form})


def delete_task(request, pk):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=pk)
        task.is_deleted = True
        task.save()
        return redirect('/reports')


def delete_report(request, pk):
    if request.method == 'GET':
        report = get_object_or_404(Report, pk=pk)
        report.is_deleted = True
        report.save()
        return redirect('/reports')
