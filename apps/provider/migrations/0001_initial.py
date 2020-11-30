# Generated by Django 3.1.1 on 2020-11-30 11:23

import functools
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import utils.shortcuts


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("account", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentAccount",
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
                ("u_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                (
                    "correlation_id",
                    models.UUIDField(default=uuid.uuid4, editable=False),
                ),
                (
                    "status",
                    models.CharField(default="TERMS_ACCEPTED", max_length=255),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.account",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentaccount_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentaccount_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "payment_account",},
        ),
        migrations.CreateModel(
            name="PaymentProvider",
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
                ("u_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                (
                    "provider_slug",
                    models.CharField(max_length=255, unique=True),
                ),
                ("display_name", models.CharField(max_length=255)),
                ("website", models.URLField(max_length=255, unique=True)),
                (
                    "logo",
                    models.FileField(
                        blank=True,
                        upload_to=functools.partial(
                            utils.shortcuts._update_filename,
                            *(),
                            **{
                                "path": "paymentproviders/logo/",
                                "prefix": "image",
                            }
                        ),
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentprovider_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentprovider_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentprovider_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "payment_provider",},
        ),
        migrations.CreateModel(
            name="TermsDocument",
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
                ("u_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                (
                    "document_type",
                    models.CharField(editable=False, max_length=255),
                ),
                ("document_file", models.JSONField()),
                ("is_active", models.BooleanField(default=True)),
                ("country", models.CharField(editable=False, max_length=2)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="termsdocument_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="termsdocument_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="provider.paymentprovider",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="termsdocument_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "terms_document",},
        ),
        migrations.CreateModel(
            name="ProviderUpdateWebhook",
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
                ("u_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("webhook_secret", models.CharField(max_length=256)),
                ("webhook_id", models.CharField(max_length=256, unique=True)),
                ("api_key", models.CharField(max_length=256)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="providerupdatewebhook_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="providerupdatewebhook_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="provider.paymentprovider",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="providerupdatewebhook_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "provider_update_webhook",},
        ),
        migrations.CreateModel(
            name="PaymentAccountOpeningCreds",
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
                ("u_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("api_key", models.TextField(blank=True)),
                (
                    "account_number",
                    models.CharField(blank=True, max_length=64),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentaccountopeningcreds_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentaccountopeningcreds_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "payment_account",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account_opening_creds",
                        to="provider.paymentaccount",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentaccountopeningcreds_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "payment_account_opening_creds",},
        ),
        migrations.CreateModel(
            name="PaymentAccountOpeningConsent",
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
                ("u_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("user_agent", models.TextField()),
                ("ip", models.GenericIPAddressField()),
                ("consent_timestamp", models.BigIntegerField()),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentaccountopeningconsent_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentaccountopeningconsent_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "payment_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="provider.paymentaccount",
                    ),
                ),
                (
                    "term",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="provider.termsdocument",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentaccountopeningconsent_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "payment_account_opening_consent",},
        ),
        migrations.AddField(
            model_name="paymentaccount",
            name="provider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="provider.paymentprovider",
            ),
        ),
        migrations.AddField(
            model_name="paymentaccount",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="paymentaccount_updated_by_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="PaymentProviderCred",
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
                ("u_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("api_environment", models.CharField(max_length=255)),
                ("api_password", models.CharField(blank=True, max_length=255)),
                ("api_key", models.CharField(blank=True, max_length=255)),
                ("api_login_id", models.CharField(blank=True, max_length=255)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentprovidercred_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentprovidercred_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="provider.paymentprovider",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentprovidercred_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "payment_provider_cred",
                "unique_together": {("provider", "api_environment")},
            },
        ),
        migrations.CreateModel(
            name="PaymentProviderAuth",
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
                ("u_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("auth_token", models.CharField(max_length=1024)),
                ("expires_at", models.DateTimeField()),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentproviderauth_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentproviderauth_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "provider",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="provider.paymentprovider",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paymentproviderauth_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "payment_provider_auth",
                "unique_together": {("provider", "auth_token", "expires_at")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="paymentaccount", unique_together={("account", "provider")},
        ),
    ]
