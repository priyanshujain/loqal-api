# Generated by Django 3.1.5 on 2021-03-11 08:40

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import db.models.fields.choice


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0046_auto_20210211_1405"),
        ("account", "0027_auto_20210212_1239"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notification", "0006_auto_20210104_0443"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffPaymentNotificationSetting",
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
                ("phone_number", models.CharField(blank=True, max_length=10)),
                (
                    "phone_number_country",
                    models.CharField(blank=True, default="US", max_length=2),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "notitication_type",
                    db.models.fields.choice.ChoiceCharEnumField(
                        max_length=128
                    ),
                ),
                ("sms_enabled", models.BooleanField(default=False)),
                ("email_enabled", models.BooleanField(default=False)),
                ("app_enabled", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="staffpaymentnotificationsetting_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="staffpaymentnotificationsetting_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.merchantaccount",
                    ),
                ),
                (
                    "staff",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="merchant.accountmember",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="staffpaymentnotificationsetting_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "staff_payment_notification_setting",
            },
        ),
    ]
