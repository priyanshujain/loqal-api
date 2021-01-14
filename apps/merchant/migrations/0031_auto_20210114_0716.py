# Generated by Django 3.1.5 on 2021-01-14 07:16

from django.db import migrations, models

import db.models.fields.choice


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0030_auto_20210114_0408"),
    ]

    operations = [
        migrations.AddField(
            model_name="codesandprotocols",
            name="cleaning_frequency",
            field=db.models.fields.choice.ChoiceCharEnumField(
                default="not_provided", max_length=32
            ),
        ),
        migrations.AlterField(
            model_name="codesandprotocols",
            name="last_cleaned_at",
            field=models.DateTimeField(null=True),
        ),
    ]
