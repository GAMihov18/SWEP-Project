# Generated by Django 5.1.3 on 2025-01-15 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_news_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='address',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
