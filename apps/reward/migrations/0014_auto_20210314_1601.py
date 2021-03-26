# Generated by Django 3.1.5 on 2021-03-14 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reward", "0013_auto_20210308_1135"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rewardusageitem",
            name="voucher_reward",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="usages",
                to="reward.voucherreward",
            ),
        ),
    ]
