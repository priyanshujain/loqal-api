# Generated by Django 3.1.1 on 2020-12-23 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0012_auto_20201223_1310"),
    ]

    operations = [
        migrations.RenameField(
            model_name="transaction",
            old_name="tranasction_type",
            new_name="transaction_type",
        ),
    ]
