# Generated by Django 3.1.1 on 2020-12-30 13:21

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import db.models.fields.choice


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserDevice",
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
                ("active", models.BooleanField(default=True)),
                (
                    "device_tracking_id",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "registration_id",
                    models.TextField(verbose_name="Registration token"),
                ),
                (
                    "device_type",
                    db.models.fields.choice.ChoiceCharEnumField(max_length=8),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "user_device",
            },
        ),
    ]
