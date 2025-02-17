# Generated by Django 3.1.5 on 2021-03-10 03:47

import django.contrib.postgres.fields
from django.db import migrations, models


def migrate_data(apps, schema_editor):
    FeatureAccessRole = apps.get_model("merchant", "FeatureAccessRole")
    for role in FeatureAccessRole.objects.all():
        if role.is_full_access:
            role.top_customers = []


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0051_auto_20210310_0347"),
    ]

    operations = [
        migrations.RunPython(migrate_data),
    ]
