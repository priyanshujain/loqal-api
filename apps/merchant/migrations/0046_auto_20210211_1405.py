# Generated by Django 3.1.5 on 2021-02-11 14:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "merchant",
            "0045_remove_incorporationverificationdocument_verification_document_type",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="accountmember",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="merchant_account_member",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
