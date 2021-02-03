# Generated by Django 3.1.5 on 2021-02-03 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0044_transaction_is_receiver_tranfer_complete"),
        ("metrics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="merchanttoconsumerrating",
            name="transaction",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="merchant_rating",
                to="payment.transaction",
            ),
        ),
    ]
