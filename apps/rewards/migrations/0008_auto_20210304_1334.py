# Generated by Django 3.1.5 on 2021-03-04 13:34

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import db.models.fields.choice


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("account", "0027_auto_20210212_1239"),
        ("rewards", "0007_auto_20210303_1541"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rewardusage",
            name="total_amount",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=6, null=True
            ),
        ),
        migrations.AlterField(
            model_name="rewardusageitem",
            name="amount",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=6, null=True
            ),
        ),
        migrations.CreateModel(
            name="RewardsEvent",
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
                (
                    "event_type",
                    db.models.fields.choice.ChoiceCharEnumField(max_length=32),
                ),
                (
                    "reward_value_type",
                    db.models.fields.choice.ChoiceCharEnumField(max_length=32),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=6
                    ),
                ),
                (
                    "consumer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reward_events",
                        to="account.consumeraccount",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rewardsevent_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rewardsevent_deleted_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reward_events",
                        to="account.merchantaccount",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rewardsevent_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "rewards_event",
            },
        ),
    ]
