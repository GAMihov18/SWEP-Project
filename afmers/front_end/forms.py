from django.contrib.auth.forms import UserCreationForm
from django import forms
from api.models import Account


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "email",
            "phone_number",
            "address",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form widgets or attributes if needed
        self.fields["username"].widget.attrs.update({"placeholder": "Enter username"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter email"})
        self.fields["phone_number"].widget.attrs.update(
            {"placeholder": "Enter phone number"}
        )
        self.fields["address"].widget.attrs.update({"placeholder": "Enter address"})
