from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize
from django.utils.timezone import now
import uuid
import json

# Create your models here.


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


AUTHORITY_LEVEL = [
    ("N", "None"),
    ("L", "Logged In"),
    ("E", "Emergency Worker"),
    ("O", "Organizer"),
    ("A", "Admin"),
]
"""
N: None
L: Logged In
E: Emergency Worker
O: Organizer
A: Admin
"""


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
    address = models.CharField(max_length=300, blank=True, null=True)
    authority_level = models.CharField(
        max_length=1, choices=AUTHORITY_LEVEL, default="N", blank=False
    )

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
                "authority_level": self.authority_level,
            }
        )
        return data

    @classmethod
    def from_json(cls, json_data):
        """Override from_json to parse Account-specific fields."""
        data = json.loads(json_data)
        data["phone_number"] = data.get("phone_number", None)
        data["address"] = data.get("address", None)
        data["authority_level"] = data.get("authority_level", "N")
        return cls(**data)


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         ("Additional Info", {"fields": ("phone_number", "address", "is_deleted")}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         ("Additional Info", {"fields": ("phone_number", "address")}),
#     )


class Report(BaseModel):
    """
    api.models.Report(BaseModel)
        account -> ForeignKey
        title -> CharField
        descirption -> CharField
        date_reported -> DateField
        time_reported -> TimeField
        status -> CharField
        has_task -> BooleanField
    """

    account = models.ForeignKey("api.Account", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=300, blank=True)
    date_reported = models.DateField(blank=False, default=now)
    time_reported = models.TimeField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_OPTIONS, default="N", blank=False
    )
    has_task = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=False, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.title

    def to_json(self):
        """Override to_json to include custom fields for Report."""
        data = super().to_json()
        data.update(
            {
                "account": str(self.account_id.id),
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
        data["account"] = Account.objects.get(
            id=data["account"]
        )  # Ensure we resolve the ForeignKey
        data["date_reported"] = data.get("date_reported", None)
        return cls(**data)


class Task(BaseModel):
    """
    api.models.Task(BaseModel)
        report -> ForeignKey
        title -> CharField
        descirption -> CharField
        status -> CharField
    """
    username = models.ForeignKey(to=Account, to_field="username", on_delete=models.CASCADE, null=True)
    report = models.ForeignKey(to=Report, on_delete=models.CASCADE)
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
                "report": str(self.report.id),
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
        data["report"] = Report.objects.get(id=data["report"])  # Resolve ForeignKey
        return cls(**data)


class Request(BaseModel):
    requestee = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    reasons = models.TextField()
    requested_level = models.CharField(
        max_length=1, choices=AUTHORITY_LEVEL, default="N", blank=False
    )
    is_approved = models.BooleanField(null=True)

    def __str__(self):
        return self.requested_level

    def to_json(self):
        data = super().to_json()
        data.update(
            {
                "requestee": str(self.requestee.id),
                "reasons": self.reasons,
                "requested_level": self.requested_level,
            }
        )
        return data

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        data["requestee"] = Account.objects.get(id=data["requestee"])
        return cls(**data)


class News(BaseModel):
    """
    api.models.Report(BaseModel)
        account -> ForeignKey
        title -> CharField
        descirption -> CharField
        date -> DateField
        time -> TimeField
        status -> CharField
    """

    account = models.ForeignKey("api.Account", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=300, blank=True)
    date = models.DateField(blank=False, default=now)
    time = models.TimeField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_OPTIONS, default="N", blank=False
    )
    address = models.CharField(max_length=255, blank=True, null=True, default=None)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.title

    def to_json(self):
        """Override to_json to include custom fields for Report."""
        data = super().to_json()
        data.update(
            {
                "account": str(self.account_id.id),
                "title": self.title,
                "description": self.description,
                "date": str(self.date),
                "time_reported": (
                    str(self.time) if self.time else None
                ),
                "status": self.status,
            }
        )
        return data

    @classmethod
    def from_json(cls, json_data):
        """Override from_json to parse Report-specific fields."""
        data = json.loads(json_data)
        data["account"] = Account.objects.get(
            id=data["account"]
        )  # Ensure we resolve the ForeignKey
        data["date"] = data.get("date", None)
        return cls(**data)
