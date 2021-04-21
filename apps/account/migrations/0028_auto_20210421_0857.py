# Generated by Django 3.1.5 on 2021-04-21 08:57

import timezone_field.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0027_auto_20210212_1239"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumeraccount",
            name="tz",
            field=timezone_field.fields.TimeZoneField(default="Europe/London"),
        ),
        migrations.AddField(
            model_name="merchantaccount",
            name="tz",
            field=timezone_field.fields.TimeZoneField(default="US/Eastern"),
        ),
    ]
