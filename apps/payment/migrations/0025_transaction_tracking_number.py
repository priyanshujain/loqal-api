# Generated by Django 3.1.1 on 2020-12-25 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0024_transaction_individual_ach_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="tracking_number",
            field=models.CharField(
                blank=True,
                default=None,
                editable=False,
                max_length=10,
                null=True,
                unique=True,
            ),
        ),
    ]
