# Generated by Django 3.1.1 on 2020-12-31 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("notification", "0002_auto_20201231_1535"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userdevice",
            old_name="registration_id",
            new_name="fcm_token",
        ),
    ]
