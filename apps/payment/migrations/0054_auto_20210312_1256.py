# Generated by Django 3.1.5 on 2021-03-12 12:56

import django.db.models.deletion
from django.db import migrations, models

import db.models.fields.choice
import db.models.fields.enum


class Migration(migrations.Migration):

    dependencies = [
        ("reward", "0013_auto_20210308_1135"),
        ("payment", "0053_auto_20210312_0735"),
    ]

    operations = [
        migrations.AddField(
            model_name="directmerchantpayment",
            name="status",
            field=db.models.fields.enum.ChoiceEnumField(default=0),
        ),
        migrations.AddField(
            model_name="paymentevent",
            name="transfer_type",
            field=db.models.fields.choice.ChoiceCharEnumField(
                default="ach_bank_transfer", max_length=64
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="reward_usage",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="transaction",
                to="reward.rewardusage",
            ),
        ),
    ]
