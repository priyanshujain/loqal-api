# Generated by Django 3.1.5 on 2021-01-24 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0021_auto_20210123_0538"),
        ("payment", "0040_auto_20210120_1302"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="is_sender_tranfer_pending",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="paymentregister",
            name="account",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="account.account",
            ),
        ),
    ]
