# Generated by Django 3.1.5 on 2021-03-16 08:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reward", "0014_auto_20210314_1601"),
        ("order", "0013_order_total_reclaimed_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="applied_voucher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applied_orders",
                to="reward.voucherreward",
            ),
        ),
    ]
