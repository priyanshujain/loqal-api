# Generated by Django 3.1.5 on 2021-02-08 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0007_providerwebhookevent_event_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providerwebhookevent',
            name='target_resource_dwolla_id',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=255, null=True),
        ),
    ]
