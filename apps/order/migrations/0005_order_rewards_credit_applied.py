# Generated by Django 3.1.5 on 2021-03-01 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0004_auto_20210206_1637"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="rewards_credit_applied",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=6
            ),
        ),
    ]
