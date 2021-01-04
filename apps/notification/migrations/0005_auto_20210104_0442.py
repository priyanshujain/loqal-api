# Generated by Django 3.1.1 on 2021-01-04 04:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notification", "0004_auto_20210102_1107"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdevice",
            name="device_tracking_id",
            field=models.CharField(
                blank=True, default=None, max_length=32, null=True
            ),
        ),
        migrations.AlterUniqueTogether(
            name="userdevice",
            unique_together={("user", "device_id")},
        ),
    ]
