# Generated by Django 3.1.1 on 2020-12-10 10:04

import db.models.fields.enum
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20201201_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantaccount',
            name='business_contact_number',
        ),
        migrations.RemoveField(
            model_name='merchantaccount',
            name='website',
        ),
        migrations.AddField(
            model_name='merchantaccount',
            name='account_status',
            field=db.models.fields.enum.ChoiceEnumField(help_text='Status for the merchant account with dwolla.'),
        ),
    ]
