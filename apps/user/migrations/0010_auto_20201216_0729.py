# Generated by Django 3.1.1 on 2020-12-16 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0009_auto_20201216_0727"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                default=None, max_length=255, null=True, unique=True
            ),
        ),
    ]
