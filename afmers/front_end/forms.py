from django.contrib.auth.forms import UserCreationForm
from django import forms
from api.models import Account, Report, Task, News


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "password1",
            "password2",
            "authority_level"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form widgets or attributes if needed
        self.fields["username"].widget.attrs.update({"placeholder": "Enter username"})
        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter first name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Enter last name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter email"})
        self.fields["phone_number"].widget.attrs.update(
            {"placeholder": "Enter phone number"}
        )
        self.fields["address"].widget.attrs.update({"placeholder": "Enter address"})
        self.fields["authority_level"].widget.attrs.update({"placeholder": "select authority type"})


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("title",
                  "description",
                  "address"
                  )
        widgets = {
            "description": forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 300px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"placeholder": "Enter a title"})
        self.fields["description"].widget.attrs.update({"placeholder": "Description"})
        self.fields["address"].widget.attrs.update({"placeholder": "example: Getreidegasse 9, 5020 Salzburg, Austria"})

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title",
                  "descirption",
                  "username",
                  "status"
                  )
        widgets = {
            "descirption": forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 300px;'}),
        }

    username = forms.ModelChoiceField(
        queryset=Account.objects.filter(authority_level='E'),
        empty_label="Select a user",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"placeholder": "Enter a title"})
        self.fields["descirption"].widget.attrs.update({"placeholder": "Description"})
        self.fields["username"].widget.attrs.update({"placeholder": "Enter the username of the person this task is to be assigned to"})

class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('status',)

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ("title",
                  "description",
                  "address"
                  )
        widgets = {
            "description": forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 300px;'}),
            "address": forms.TextInput(attrs={'required': 'false'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"placeholder": "Enter a title"})
        self.fields["description"].widget.attrs.update({"placeholder": "Description"})
        self.fields["address"].widget.attrs.update({"placeholder": "example: Getreidegasse 9, 5020 Salzburg, Austria"})
