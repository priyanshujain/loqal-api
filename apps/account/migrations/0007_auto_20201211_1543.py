# Generated by Django 3.1.1 on 2020-12-11 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_auto_20201211_1541"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="merchantaccount",
            table="merchant_account",
        ),
    ]
