# Generated by Django 3.1.1 on 2020-12-15 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0007_auto_20201215_0913"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="merchantprofile",
            name="category",
        ),
    ]
