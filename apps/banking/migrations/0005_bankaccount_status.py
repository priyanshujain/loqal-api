# Generated by Django 3.1.5 on 2021-01-15 12:06

from django.db import migrations

import db.models.fields.choice


class Migration(migrations.Migration):

    dependencies = [
        ("banking", "0004_auto_20201211_1541"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankaccount",
            name="status",
            field=db.models.fields.choice.ChoiceCharEnumField(
                max_length=32, default="verified"
            ),
        ),
    ]
