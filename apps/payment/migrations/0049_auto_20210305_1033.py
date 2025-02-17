# Generated by Django 3.1.5 on 2021-03-05 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reward", "0010_auto_20210304_1653"),
        ("payment", "0048_merchantreceivelimit"),
    ]

    operations = [
        migrations.AddField(
            model_name="refund",
            name="reclaim_reward_value",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=6
            ),
        ),
        migrations.AddField(
            model_name="refund",
            name="requested_items_value",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=6
            ),
        ),
        migrations.AddField(
            model_name="refund",
            name="return_reward_value",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=6
            ),
        ),
        migrations.AddField(
            model_name="refund",
            name="reward_credit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="refunds",
                to="reward.rewardusage",
            ),
        ),
    ]
