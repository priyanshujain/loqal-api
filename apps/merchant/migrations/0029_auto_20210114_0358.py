# Generated by Django 3.1.5 on 2021-01-14 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("box", "0005_boxfile_in_use"),
        ("merchant", "0028_auto_20210105_1440"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="merchantprofile",
            name="hero_image",
        ),
        migrations.AddField(
            model_name="merchantprofile",
            name="avatar_file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="merchant_avatar_file",
                to="box.boxfile",
            ),
        ),
        migrations.AddField(
            model_name="merchantprofile",
            name="background_file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="merchant_background_file",
                to="box.boxfile",
            ),
        ),
    ]
