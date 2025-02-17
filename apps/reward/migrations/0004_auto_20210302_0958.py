# Generated by Django 3.1.5 on 2021-03-02 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reward", "0003_loyaltyprogram_reward_value_maximum"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cashreward",
            name="order",
        ),
        migrations.RemoveField(
            model_name="voucherreward",
            name="order",
        ),
        migrations.AddField(
            model_name="cashreward",
            name="cancellation_reason",
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name="cashreward",
            name="is_cancelled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="voucherreward",
            name="cancellation_reason",
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name="voucherreward",
            name="is_cancelled",
            field=models.BooleanField(default=False),
        ),
    ]
