# Generated by Django 5.1.3 on 2025-01-14 23:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_reporter_account_report_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
