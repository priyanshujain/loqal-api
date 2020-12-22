# Generated by Django 3.1.1 on 2020-12-22 06:47

import db.models.fields.enum
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0012_auto_20201222_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficialowner',
            name='verification_document_status',
            field=db.models.fields.enum.ChoiceEnumField(help_text='Status for the verification document with dwolla.'),
        ),
        migrations.AlterField(
            model_name='controllerdetails',
            name='verification_document_status',
            field=db.models.fields.enum.ChoiceEnumField(help_text='Status for the verification document with dwolla.'),
        ),
        migrations.AlterField(
            model_name='incorporationdetails',
            name='verification_document_status',
            field=db.models.fields.enum.ChoiceEnumField(help_text='Status for the verification document with dwolla.'),
        ),
    ]
