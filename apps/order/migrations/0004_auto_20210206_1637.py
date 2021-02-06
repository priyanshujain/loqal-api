# Generated by Django 3.1.5 on 2021-02-06 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20201229_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_net_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
