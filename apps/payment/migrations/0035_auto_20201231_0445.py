# Generated by Django 3.1.1 on 2020-12-31 04:45

import db.models.fields.choice
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0034_auto_20201230_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='refunded_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=5),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=db.models.fields.choice.ChoiceCharEnumField(default='direct_merchant_payment', max_length=32),
        ),
    ]
