# Generated by Django 3.1.1 on 2020-12-09 12:23

import uuid

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import utils.shortcuts


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("box", "0003_auto_20201207_1706"),
        ("account", "0004_auto_20201201_1137"),
    ]

    operations = [
        migrations.CreateModel(
            name="MerchantCategory",
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
                ("name", models.CharField(max_length=250)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True, max_length=255, unique=True
                    ),
                ),
                ("description", models.TextField(blank=True)),
                (
                    "background_color",
                    models.CharField(blank=True, max_length=128),
                ),
                (
                    "background_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="box.boxfile",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchantcategory_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchantcategory_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchantcategory_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "merchant_category",
            },
        ),
        migrations.CreateModel(
            name="ServiceAvailability",
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
                ("curbside_pickup", models.BooleanField(default=True)),
                ("delivery", models.BooleanField(default=True)),
                ("takeout", models.BooleanField(default=True)),
                ("sitting_dining", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="serviceavailability_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="serviceavailability_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "merchant",
                    models.OneToOneField(
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
                        related_name="serviceavailability_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "merchant_service_availability",
            },
        ),
        migrations.CreateModel(
            name="MerchantProfile",
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
                ("full_name", models.CharField(max_length=256)),
                ("about", models.TextField(blank=True)),
                ("address", models.JSONField()),
                (
                    "neighborhood",
                    models.CharField(
                        blank=True, help_text="Ex. Navy Yard", max_length=128
                    ),
                ),
                ("website", models.URLField(blank=True)),
                ("facebook_page", models.URLField(blank=True)),
                ("istagram_page", models.URLField(blank=True)),
                ("youtube_page", models.URLField(blank=True)),
                ("yelp_page", models.URLField(blank=True)),
                ("phone_number", models.CharField(max_length=15)),
                (
                    "parking_details",
                    models.TextField(
                        blank=True,
                        help_text="Where can cusotmers park their vehiclesEx. The Yards Lot Q; Limited street parking",
                    ),
                ),
                (
                    "dress_code",
                    models.CharField(
                        blank=True,
                        help_text="Ex. Smart Casual",
                        max_length=1024,
                    ),
                ),
                (
                    "dining_styles",
                    models.CharField(
                        blank=True,
                        help_text="Ex. Casual Dining",
                        max_length=1024,
                    ),
                ),
                (
                    "cuisines",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=64),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "amenities",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=64),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                ("additional_details", models.TextField(blank=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="merchant.merchantcategory",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchantprofile_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchantprofile_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "logo",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="box.boxfile",
                    ),
                ),
                (
                    "merchant",
                    models.OneToOneField(
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
                        related_name="merchantprofile_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "merchant_profile",
            },
        ),
        migrations.CreateModel(
            name="MerchantOperationHours",
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
                ("day", models.CharField(max_length=32)),
                ("open_time", models.TimeField()),
                ("close_time", models.TimeField()),
                ("is_closed", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchantoperationhours_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchantoperationhours_deleted_by_user",
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
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchantoperationhours_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="IncorporationDetails",
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
                ("legal_business_name", models.CharField(max_length=512)),
                ("ein_number", models.CharField(max_length=11)),
                ("registered_address", models.JSONField()),
                ("business_type", models.CharField(max_length=32)),
                ("business_classification", models.CharField(max_length=64)),
                (
                    "verification_document_type",
                    models.CharField(blank=True, max_length=32),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="incorporationdetails_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="incorporationdetails_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "merchant",
                    models.OneToOneField(
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
                        related_name="incorporationdetails_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "verification_document_file",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="box.boxfile",
                    ),
                ),
            ],
            options={
                "db_table": "merchant_onboarding_incorporation_details",
            },
        ),
        migrations.CreateModel(
            name="IncorporationConsent",
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
                ("first_name", models.CharField(max_length=256)),
                ("last_name", models.CharField(max_length=256)),
                ("email", models.CharField(max_length=256)),
                ("ip_address", models.GenericIPAddressField()),
                (
                    "dwolla_correlation_id",
                    models.CharField(
                        default=utils.shortcuts.generate_uuid_hex,
                        editable=False,
                        max_length=40,
                        unique=True,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="incorporationconsent_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="incorporationconsent_deleted_by_user",
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
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="incorporationconsent_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "merchant_onboarding_incorporation_consent",
            },
        ),
        migrations.CreateModel(
            name="ControllerDetails",
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
                ("first_name", models.CharField(max_length=256)),
                ("last_name", models.CharField(max_length=256)),
                ("ssn", models.CharField(blank=True, max_length=9)),
                ("dob", models.DateField()),
                ("address", models.JSONField()),
                (
                    "passport_country",
                    models.CharField(blank=True, max_length=2),
                ),
                ("passport_number", models.CharField(max_length=32)),
                (
                    "verification_document_type",
                    models.CharField(blank=True, max_length=32),
                ),
                ("title", models.CharField(max_length=256)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="controllerdetails_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="controllerdetails_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "merchant",
                    models.OneToOneField(
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
                        related_name="controllerdetails_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "verification_document_file",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="box.boxfile",
                    ),
                ),
            ],
            options={
                "db_table": "merchant_onboarding_controller_details",
            },
        ),
        migrations.CreateModel(
            name="CodesAndProtocols",
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
                ("contactless_payments", models.BooleanField(default=True)),
                ("mask_required", models.BooleanField(default=True)),
                ("sanitizer_provided", models.BooleanField(default=True)),
                ("ourdoor_seating", models.BooleanField(default=True)),
                ("last_cleaned_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="codesandprotocols_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="codesandprotocols_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "merchant",
                    models.OneToOneField(
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
                        related_name="codesandprotocols_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "merchant_codes_and_protocols",
            },
        ),
        migrations.CreateModel(
            name="BeneficialOwner",
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
                ("first_name", models.CharField(max_length=256)),
                ("last_name", models.CharField(max_length=256)),
                ("ssn", models.CharField(blank=True, max_length=9)),
                ("dob", models.DateField()),
                ("address", models.JSONField()),
                (
                    "passport_country",
                    models.CharField(blank=True, max_length=2),
                ),
                ("passport_number", models.CharField(max_length=32)),
                (
                    "verification_document_type",
                    models.CharField(blank=True, max_length=32),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="beneficialowner_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="beneficialowner_deleted_by_user",
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
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="beneficialowner_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "verification_document_file",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="box.boxfile",
                    ),
                ),
            ],
            options={
                "db_table": "merchant_onboarding_beneficial_owner",
            },
        ),
    ]
