# Generated by Django 3.1.5 on 2021-01-07 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0014_auto_20210105_1440"),
    ]

    operations = [
        migrations.AddField(
            model_name="merchantaccount",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
