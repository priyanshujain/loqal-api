# Generated by Django 3.1.1 on 2020-12-29 12:21

from django.db import migrations

import db.models.fields.enum


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0030_auto_20201229_1218"),
    ]

    operations = [
        migrations.AlterField(
            model_name="refund",
            name="status",
            field=db.models.fields.enum.ChoiceEnumField(),
        ),
    ]
