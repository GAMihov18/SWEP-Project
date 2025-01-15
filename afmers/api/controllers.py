from django.contrib.auth import authenticate, login, logout
from api.models import Account, Report, Task, Request


class BaseController:
    """Base controller with common CRUD operations"""

    model = None  # To be set by subclasses

    @classmethod
    def all(cls):
        return cls.model.objects.filter(is_deleted=False)

    @classmethod
    def get_by_id(cls, obj_id):
        return cls.model.objects.filter(id=obj_id, is_deleted=False).first()

    @classmethod
    def create(cls, data):
        return cls.model.objects.create(**data)

    @classmethod
    def update(cls, obj_id, data):
        instance = cls.model.objects.filter(id=obj_id, is_deleted=False).first()
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            instance.save()
        return instance

    @classmethod
    def delete(cls, obj_id):
        instance = cls.model.objects.filter(id=obj_id, is_deleted=False).first()
        if instance:
            instance.delete()
        return instance


class AccountController(BaseController):
    """Controller for Account model with authentication methods"""

    model = Account

    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)
        return user

    @staticmethod
    def login_user(request, user):
        if user is not None:
            login(request, user)
            return True
        return False

    @staticmethod
    def logout_user(request):
        logout(request)

    @staticmethod
    def register_user(data):
        if "password" not in data:
            raise ValueError("Password is required for registration.")
        password = data.pop("password")
        account = Account.objects.create_user(**data)
        account.set_password(password)
        account.save()
        return account


class ReportController(BaseController):
    """Controller for Report model"""

    model = Report

    @staticmethod
    def get_by_account(account):
        return Report.objects.filter(account=account, is_deleted=False)

    @staticmethod
    def mark_as_with_task(report_id):
        report = Report.objects.filter(id=report_id, is_deleted=False).first()
        if report:
            report.has_task = True
            report.save()
        return report


class TaskController(BaseController):
    """Controller for Task model"""

    model = Task

    @staticmethod
    def get_by_report(report):
        return Task.objects.filter(report=report, is_deleted=False)


class RequestController(BaseController):
    """Controller for Request model"""

    model = Request

    @staticmethod
    def approve_request(request_id):
        request = Request.objects.filter(id=request_id, is_deleted=False).first()
        if request:
            request.is_approved = True
            request.save()
        return request

    @staticmethod
    def deny_request(request_id):
        request = Request.objects.filter(id=request_id, is_deleted=False).first()
        if request:
            request.is_approved = False
            request.save()
        return request
