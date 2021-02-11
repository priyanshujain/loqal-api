# Generated by Django 3.1.5 on 2021-02-11 09:31

import db.models.fields.choice
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210210_0716'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantMetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('platform', db.models.fields.choice.ChoiceCharEnumField(max_length=8)),
                ('primary_banking_verification_provider', db.models.fields.choice.ChoiceCharEnumField(default='plaid', max_length=32)),
            ],
            options={
                'db_table': 'merchant_metadata',
            },
        ),
        migrations.AddField(
            model_name='appmetadata',
            name='primary_banking_verification_provider',
            field=db.models.fields.choice.ChoiceCharEnumField(default='plaid', max_length=32),
        ),
    ]
