# Generated by Django 3.1.5 on 2021-01-27 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("provider", "0006_auto_20210108_0904"),
    ]

    operations = [
        migrations.AddField(
            model_name="providerwebhookevent",
            name="event_timestamp",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
