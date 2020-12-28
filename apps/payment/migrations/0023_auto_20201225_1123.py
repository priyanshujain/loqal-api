# Generated by Django 3.1.1 on 2020-12-25 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0022_auto_20201225_1104"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="refund",
            name="order",
        ),
        migrations.AddField(
            model_name="refund",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="refunds",
                to="payment.payment",
            ),
        ),
        migrations.AlterModelTable(
            name="refund",
            table="payment_refund",
        ),
    ]
