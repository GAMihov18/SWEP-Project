# services/report_service.py
from api.models import Account, Report, Task

"""
Access data/models/classes using these classes
"""


class AccountService:
    """Service over Account model"""

    @staticmethod
    def all():
        """Returns all accounts"""
        return Account.objects.filter(is_deleted=False)

    @staticmethod
    def filter(*args, **kwargs):
        """Filters accounts based on conditions"""
        kwargs.setdefault("is_deleted", False)
        return Account.objects.filter(*args, **kwargs)

    @staticmethod
    def get_by_id(account_id):
        """Retrieve a single account by ID"""
        return AccountService.filter(id=account_id).first()

    @staticmethod
    def create(account_data):
        """
        Create a new account from a dictionary or another Account object.
        """
        if isinstance(account_data, Account):
            # Convert a model instance to a dictionary, excluding auto fields like id
            account_data = {
                field.name: getattr(account_data, field.name)
                for field in account_data._meta.fields
                if field.name != "id"
            }
        elif not isinstance(account_data, dict):
            raise ValueError(
                "account_data must be an Account instance or a dictionary."
            )

        # Create the new Account instance
        return Account.objects.create(**account_data)

    @staticmethod
    def update(account_data):
        """
        Update an account from a dictionary or another Account object. Find by id.
        """
        if isinstance(account_data, Account):
            account_id = account_data.id
            updated_fields = {
                field.name: getattr(account_data, field.name)
                for field in account_data._meta.fields
                if field.name != "id"
            }
        elif isinstance(account_data, dict) and "id" in account_data:
            account_id = account_data["id"]
            updated_fields = {k: v for k, v in account_data.items() if k != "id"}
        else:
            raise ValueError("account_data must have an 'id' field.")

        # Update the Account instance
        Account.objects.filter(id=account_id).update(**updated_fields)
        return Account.objects.get(id=account_id)

    @staticmethod
    def delete(account_id):
        """Delete an account by ID"""
        AccountService.filter(id=account_id).delete()


class ReportService:
    """Service over Report model"""

    @staticmethod
    def all():
        """Returns all non-deleted reports"""
        return Report.objects.filter(is_deleted=False)

    @staticmethod
    def filter(*args, **kwargs):
        """Filters non-deleted reports"""
        kwargs.setdefault("is_deleted", False)
        return Report.objects.filter(*args, **kwargs)

    @staticmethod
    def get_by_user(user):
        """Returns all reports created by user"""
        return ReportService.filter(reporter_account=user)

    @staticmethod
    def get_with_tasks():
        """Returns all reports that have attached tasks"""
        return ReportService.filter(has_task=True)

    @staticmethod
    def create(report_data):
        """
        Create a new report from a dictionary or another Report object.
        """
        if isinstance(report_data, Report):
            # Convert a model instance to a dictionary, excluding auto fields like id
            report_data = {
                field.name: getattr(report_data, field.name)
                for field in report_data._meta.fields
                if field.name != "id"
            }
        elif not isinstance(report_data, dict):
            raise ValueError("report_data must be a Report instance or a dictionary.")

        # Create the new Report instance
        return Report.objects.create(**report_data)

    @staticmethod
    def update(report_data):
        """
        Update the report from a dictionary or another Report object. Find by id
        """
        if isinstance(report_data, Report):
            report_id = report_data.id
            updated_fields = {
                field.name: getattr(report_data, field.name)
                for field in report_data._meta.fields
                if field.name != "id"
            }
        elif isinstance(report_data, dict) and "id" in report_data:
            report_id = report_data["id"]
            updated_fields = {k: v for k, v in report_data.items() if k != "id"}
        else:
            raise ValueError("report_data must have an 'id' field.")

        # Update the Report instance
        Report.objects.filter(id=report_id).update(**updated_fields)
        return Report.objects.get(id=report_id)

    @staticmethod
    def delete(report_id):
        """
        Soft-delete a report by setting is_deleted to True
        """
        report = Report.objects.filter(id=report_id).first()
        if report:
            report.is_deleted = True
            report.save()
        return report


class TaskService:
    """Service over Task model"""

    @staticmethod
    def all():
        """Returns all tasks"""
        return Task.objects.filter(is_deleted=False)

    @staticmethod
    def filter(*args, **kwargs):
        """Filters tasks based on conditions"""
        kwargs.setdefault("is_deleted", False)
        return Task.objects.filter(*args, **kwargs)

    @staticmethod
    def get_by_report(report):
        """Returns all tasks associated with a specific report"""
        return TaskService.filter(report=report)

    @staticmethod
    def create(task_data):
        """
        Create a new task from a dictionary or another Task object.
        """
        if isinstance(task_data, Task):
            # Convert a model instance to a dictionary, excluding auto fields like id
            task_data = {
                field.name: getattr(task_data, field.name)
                for field in task_data._meta.fields
                if field.name != "id"
            }
        elif not isinstance(task_data, dict):
            raise ValueError("task_data must be a Task instance or a dictionary.")

        # Create the new Task instance
        return Task.objects.create(**task_data)

    @staticmethod
    def update(task_data):
        """
        Update the task from a dictionary or another Task object. Find by id
        """
        if isinstance(task_data, Task):
            task_id = task_data.id
            updated_fields = {
                field.name: getattr(task_data, field.name)
                for field in task_data._meta.fields
                if field.name != "id"
            }
        elif isinstance(task_data, dict) and "id" in task_data:
            task_id = task_data["id"]
            updated_fields = {k: v for k, v in task_data.items() if k != "id"}
        else:
            raise ValueError("task_data must have an 'id' field.")

        # Update the Task instance

        Task.objects.filter(id=task_id).update(**updated_fields)
        return Task.objects.get(id=task_id)

    @staticmethod
    def delete(task_id):
        """
        Delete a task by id
        """
        TaskService.filter(id=task_id).delete()
