# Generated by Django 3.1.1 on 2020-12-17 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0008_auto_20201217_1008"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paymentrequest",
            name="tip_amount",
        ),
    ]
