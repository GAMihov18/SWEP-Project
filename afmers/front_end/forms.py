from django.contrib.auth.forms import UserCreationForm
from django import forms
from api.models import Account, Report


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


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("title",
                  "description"
                  )
        widgets = {
            "description": forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 300px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"placeholder": "Enter a title"})
        self.fields["description"].widget.attrs.update({"placeholder": "Description"})
