# Generated by Django 3.1.5 on 2021-03-01 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rewards", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="cashreward",
            table="cash_reward",
        ),
        migrations.AlterModelTable(
            name="loyaltyprogram",
            table="loyalty_program",
        ),
        migrations.AlterModelTable(
            name="rewardusage",
            table="reward_usage",
        ),
        migrations.AlterModelTable(
            name="rewardusageitem",
            table="reward_usage_item",
        ),
        migrations.AlterModelTable(
            name="voucherreward",
            table="voucher_reward",
        ),
    ]
