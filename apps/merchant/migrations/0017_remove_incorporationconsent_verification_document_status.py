# Generated by Django 3.1.1 on 2020-12-22 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0016_auto_20201222_0700"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="incorporationconsent",
            name="verification_document_status",
        ),
    ]
