# Generated by Django 3.1.1 on 2021-01-02 12:30

from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0035_auto_20201231_0445"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="total_tip_amount",
            field=models.DecimalField(
                decimal_places=2, default=Decimal("0.0"), max_digits=5
            ),
        ),
    ]
