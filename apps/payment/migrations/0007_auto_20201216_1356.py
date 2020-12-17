# Generated by Django 3.1.1 on 2020-12-16 13:56

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("account", "0009_remove_merchantaccount_company_name"),
        ("merchant", "0009_auto_20201216_0711"),
        ("payment", "0006_transaction_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentQrCode",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "u_id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("currency", models.CharField(default="USD", max_length=3)),
                ("qrcode_id", models.CharField(max_length=10, unique=True)),
                ("is_expired", models.BooleanField(default=False)),
                (
                    "cashier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="merchant.accountmember",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentqrcode_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentqrcode_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.merchantaccount",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentqrcode_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "payment_qrcode",
                "unique_together": {("merchant", "cashier")},
            },
        ),
        migrations.AddField(
            model_name="transaction",
            name="payment_qrcode",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="payment.paymentqrcode",
            ),
        ),
    ]
