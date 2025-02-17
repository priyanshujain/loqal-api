2  # Generated by Django 3.1.5 on 2021-03-02 10:59

from django.db import migrations, models

from apps.payment.options import PaymentStatus


def migrate_data(apps, schema_editor):
    Order = apps.get_model("order", "Order")
    for order in Order.objects.all():
        try:
            payment = order.payment
            if payment.status == PaymentStatus.CAPTURED:
                order.is_paid = True
                order.save()
        except Exception:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0009_auto_20210302_1055"),
    ]

    operations = [
        migrations.RunPython(migrate_data),
    ]
