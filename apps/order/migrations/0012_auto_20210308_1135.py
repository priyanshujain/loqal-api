# Generated by Django 3.1.5 on 2021-03-08 11:35

import db.models.fields.choice
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_order_discount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount_type',
            field=db.models.fields.choice.ChoiceCharEnumField(max_length=32),
        ),
    ]
