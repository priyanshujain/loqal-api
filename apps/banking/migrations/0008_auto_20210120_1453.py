# Generated by Django 3.1.5 on 2021-01-20 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("banking", "0007_auto_20210115_1208"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bankaccount",
            old_name="status",
            new_name="plaid_status",
        ),
    ]
