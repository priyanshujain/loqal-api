# Generated by Django 3.1.5 on 2021-03-15 03:56

import django.contrib.postgres.fields
from django.db import migrations, models


def migrate_data(apps, schema_editor):
    FeatureAccessRole = apps.get_model("merchant", "FeatureAccessRole")
    for role in FeatureAccessRole.objects.all():
        if role.is_full_access:
            role.top_customers = ["VIEW"]
            role.loyalty_program = ["CREATE", "UPDATE", "DELETE"]
            role.save()


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0052_auto_20210310_0349"),
    ]

    operations = [
        migrations.RunPython(migrate_data),
    ]
