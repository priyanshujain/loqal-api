# Generated by Django 3.1.1 on 2020-12-14 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reference", "0002_auto_20201214_1118"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="country",
            options={},
        ),
        migrations.AlterModelOptions(
            name="zipcode",
            options={},
        ),
        migrations.AlterModelTable(
            name="city",
            table="city",
        ),
        migrations.AlterModelTable(
            name="country",
            table="country",
        ),
        migrations.AlterModelTable(
            name="regionstate",
            table="region_state",
        ),
        migrations.AlterModelTable(
            name="zipcode",
            table="zip_code",
        ),
    ]
