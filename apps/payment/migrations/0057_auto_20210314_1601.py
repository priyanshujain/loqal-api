# Generated by Django 3.1.5 on 2021-03-14 16:01

from django.db import migrations

import db.models.fields.choice


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0056_auto_20210313_0926"),
    ]

    operations = [
        migrations.AlterField(
            model_name="refund",
            name="refund_reason",
            field=db.models.fields.choice.ChoiceCharEnumField(max_length=256),
        ),
    ]
