from django.test import TestCase
from api.models import Account, Report, Task
from api.controllers import AccountService, ReportService, TaskService


class AccountServiceTest(TestCase):
    def setUp(self):
        # Create sample accounts for testing
        self.account1 = Account.objects.create(
            username="user1", email="user1@example.com"
        )
        self.account2 = Account.objects.create(
            username="user2", email="user2@example.com"
        )

    def test_all_accounts(self):
        accounts = AccountService.all()
        self.assertEqual(len(accounts), 2)

    def test_filter_accounts(self):
        accounts = AccountService.filter(username="user1")
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0].email, "user1@example.com")

    def test_get_by_id(self):
        account = AccountService.get_by_id(self.account1.id)
        self.assertEqual(account.username, "user1")

    def test_create_account(self):
        data = {"username": "user3", "email": "user3@example.com"}
        new_account = AccountService.create(data)
        self.assertEqual(new_account.username, "user3")

    def test_update_account(self):
        data = {"id": self.account1.id, "email": "new_user1@example.com"}
        updated_account = AccountService.update(data)
        self.assertEqual(updated_account.email, "new_user1@example.com")

    def test_delete_account(self):
        AccountService.delete(self.account1.id)
        self.assertFalse(Account.objects.filter(id=self.account1.id).exists())


class ReportServiceTest(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.account = Account.objects.create(
            username="testuser", email="testuser@example.com"
        )
        self.report1 = Report.objects.create(
            account=self.account, title="Flood Report 1"
        )
        self.report2 = Report.objects.create(
            account=self.account, title="Flood Report 2", is_deleted=True
        )

    def test_all_reports(self):
        reports = ReportService.all()
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].title, "Flood Report 1")


class TaskServiceTest(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.account = Account.objects.create(
            username="testuser", email="testuser@example.com"
        )
        self.report = Report.objects.create(
            account=self.account, title="Report with Task"
        )
        self.task1 = Task.objects.create(title="Task 1", report=self.report)

    def test_all_tasks(self):
        tasks = TaskService.all()
        self.assertEqual(len(tasks), 1)

    def test_get_by_report(self):
        tasks = TaskService.get_by_report(self.report)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Task 1")
