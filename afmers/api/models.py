from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class BaseModel(models.Model):
    """
    api.models.BaseModel
        id -> UUID4
        is_deleted -> Boolean
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(default=False)

    def check_is_deleted(self):
        return self.is_deleted

    def delete(self):
        self.is_deleted = True

    class Meta:
        abstract = True


class Account(AbstractUser, BaseModel):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # authority_level

    def __str__(self):
        return self.username


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         ("Additional Info", {"fields": ("phone_number", "address", "is_deleted")}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         ("Additional Info", {"fields": ("phone_number", "address")}),
#     )

STATUS_OPTIONS = [
    ("N", "None"),
    ("I", "Idle"),
    ("D", "Done"),
    ("O", "Old"),
    ("V", "Voided"),
]
"""
N: None
I: Idle
D: Done
O: Old
V: Voided
"""


class Report(BaseModel):
    """
    api.models.Report(BaseModel)
        user_id -> ForeignKey
        title -> CharField
        descirption -> CharField
        date_reported -> DateField
        time_reported -> TimeField
        status -> CharField
        has_task -> BooleanField
    """

    account_id = models.ForeignKey("api.Account", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    descirption = models.CharField(max_length=300, blank=True)
    date_reported = models.DateField(blank=False)
    time_reported = models.TimeField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_OPTIONS, default="N", blank=False
    )
    has_task = models.BooleanField(default=False)


class Task(BaseModel):
    """
    api.models.Task(BaseModel)
        report_id -> ForeignKey
        title -> CharField
        descirption -> CharField
        status -> CharField
    """

    report_id = models.ForeignKey(to=Report, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    descirption = models.CharField(max_length=300, blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS_OPTIONS, default="N", blank=False
    )
