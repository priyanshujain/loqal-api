# Generated by Django 3.1.5 on 2021-01-27 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("banking", "0012_bankaccount_is_dwolla_removed"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankaccount",
            name="is_reverification_needed",
            field=models.BooleanField(default=False),
        ),
    ]
