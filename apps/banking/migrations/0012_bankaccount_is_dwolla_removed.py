# Generated by Django 3.1.5 on 2021-01-24 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("banking", "0011_auto_20210122_1625"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankaccount",
            name="is_dwolla_removed",
            field=models.BooleanField(default=False),
        ),
    ]
