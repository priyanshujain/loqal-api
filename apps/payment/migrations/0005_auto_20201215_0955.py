# Generated by Django 3.1.1 on 2020-12-15 09:55

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import db.models.fields.enum


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("account", "0008_consumeraccount_username"),
        ("payment", "0004_auto_20201211_1553"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="status",
        ),
        migrations.CreateModel(
            name="PaymentRequest",
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
                ("payment_amount", models.FloatField()),
                ("tip_amount", models.FloatField(default=0)),
                (
                    "payment_currency",
                    models.CharField(default="USD", max_length=3),
                ),
                ("fee_amount", models.FloatField(default=0.0)),
                (
                    "fee_currency",
                    models.CharField(default="USD", max_length=3),
                ),
                ("status", db.models.fields.enum.ChoiceEnumField(default=0)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="account.account",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentrequest_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentrequest_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "requested_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="requested_to_account",
                        to="account.account",
                    ),
                ),
                (
                    "transaction",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payment.transaction",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentrequest_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "payment_request",
            },
        ),
    ]
