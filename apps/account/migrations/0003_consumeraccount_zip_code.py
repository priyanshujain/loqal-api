# Generated by Django 3.1.1 on 2020-12-01 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_auto_20201130_1648"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumeraccount",
            name="zip_code",
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
