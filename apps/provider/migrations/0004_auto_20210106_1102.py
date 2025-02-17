# Generated by Django 3.1.1 on 2021-01-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("provider", "0003_providerwebhook_providerwebhookevent"),
    ]

    operations = [
        migrations.AddField(
            model_name="providerwebhook",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="providerwebhookevent",
            name="dwolla_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="providerwebhookevent",
            name="is_processed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="providerwebhookevent",
            name="target_resource_dwolla_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="providerwebhookevent",
            name="topic",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
