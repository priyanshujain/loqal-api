# Generated by Django 3.1.5 on 2021-01-14 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0038_remove_codesandprotocols_contactless_payments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="merchantprofile",
            name="neighborhood",
        ),
    ]
