# Generated by Django 3.1.1 on 2020-12-03 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0002_auto_20201202_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='is_primary',
            field=models.BooleanField(default=True),
        ),
    ]
