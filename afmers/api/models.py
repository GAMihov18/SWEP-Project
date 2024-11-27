from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize
import uuid
import json

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

    def to_json(self):
        """Convert BaseModel (and inherited models) to a JSON-compatible dictionary."""
        return {
            "id": str(self.id),
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_json(cls, json_data):
        """Create a model instance from JSON data."""
        data = json.loads(json_data)
        instance = cls(**data)
        return instance

    class Meta:
        abstract = True


class Account(AbstractUser, BaseModel):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # authority_level

    def __str__(self):
        return self.username

    def to_json(self):
        """Override to_json to include custom fields for Account."""
        data = super().to_json()
        data.update(
            {
                "username": self.username,
                "email": self.email,
                "phone_number": self.phone_number,
                "address": self.address,
            }
        )
        return data

    @classmethod
    def from_json(cls, json_data):
        """Override from_json to parse Account-specific fields."""
        data = json.loads(json_data)
        data["phone_number"] = data.get("phone_number", None)
        data["address"] = data.get("address", None)
        return cls(**data)


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

    reporter_account = models.ForeignKey("api.Account", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    descirption = models.CharField(max_length=300, blank=True)
    date_reported = models.DateField(blank=False)
    time_reported = models.TimeField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_OPTIONS, default="N", blank=False
    )
    has_task = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def to_json(self):
        """Override to_json to include custom fields for Report."""
        data = super().to_json()
        data.update(
            {
                "account_id": str(self.account_id.id),
                "title": self.title,
                "descirption": self.descirption,
                "date_reported": str(self.date_reported),
                "time_reported": (
                    str(self.time_reported) if self.time_reported else None
                ),
                "status": self.status,
                "has_task": self.has_task,
            }
        )
        return data

    @classmethod
    def from_json(cls, json_data):
        """Override from_json to parse Report-specific fields."""
        data = json.loads(json_data)
        data["account_id"] = Account.objects.get(
            id=data["account_id"]
        )  # Ensure we resolve the ForeignKey
        data["date_reported"] = data.get("date_reported", None)
        return cls(**data)


class Task(BaseModel):
    """
    api.models.Task(BaseModel)
        report_id -> ForeignKey
        title -> CharField
        descirption -> CharField
        status -> CharField
    """

    report_owner = models.ForeignKey(to=Report, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    descirption = models.CharField(max_length=300, blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS_OPTIONS, default="N", blank=False
    )

    def __str__(self):
        return self.title

    def to_json(self):
        """Override to_json to include custom fields for Task."""
        data = super().to_json()
        data.update(
            {
                "report_id": str(self.report_id.id),
                "title": self.title,
                "descirption": self.descirption,
                "status": self.status,
            }
        )
        return data

    @classmethod
    def from_json(cls, json_data):
        """Override from_json to parse Task-specific fields."""
        data = json.loads(json_data)
        data["report_id"] = Report.objects.get(
            id=data["report_id"]
        )  # Resolve ForeignKey
        return cls(**data)
