# Generated by Django 3.1.1 on 2020-12-22 16:07

from django.db import migrations, models

import db.models.fields.choice


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0020_auto_20201222_1100"),
    ]

    operations = [
        migrations.AddField(
            model_name="beneficialowner",
            name="dwolla_document_id",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="controllerdetails",
            name="dwolla_document_id",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="incorporationdetails",
            name="dwolla_document_id",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name="beneficialowner",
            name="verification_document_type",
            field=db.models.fields.choice.ChoiceCharEnumField(
                blank=True, max_length=32
            ),
        ),
        migrations.AlterField(
            model_name="controllerdetails",
            name="verification_document_type",
            field=db.models.fields.choice.ChoiceCharEnumField(
                blank=True, max_length=32
            ),
        ),
        migrations.AlterField(
            model_name="incorporationdetails",
            name="business_type",
            field=db.models.fields.choice.ChoiceCharEnumField(max_length=32),
        ),
        migrations.AlterField(
            model_name="incorporationdetails",
            name="verification_document_type",
            field=db.models.fields.choice.ChoiceCharEnumField(
                blank=True, max_length=32
            ),
        ),
    ]
