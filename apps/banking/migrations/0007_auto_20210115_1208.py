# Generated by Django 3.1.5 on 2021-01-15 12:08

from django.db import migrations

import db.models.fields.choice


class Migration(migrations.Migration):

    dependencies = [
        ("banking", "0006_auto_20210115_1207"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankaccount",
            name="status",
            field=db.models.fields.choice.ChoiceCharEnumField(max_length=32),
        ),
    ]
