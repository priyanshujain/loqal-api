# Generated by Django 3.1.1 on 2020-12-15 09:55

import db.models.fields.enum
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_auto_20201215_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=db.models.fields.enum.ChoiceEnumField(default=0),
        ),
    ]
