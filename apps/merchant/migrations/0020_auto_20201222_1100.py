# Generated by Django 3.1.1 on 2020-12-22 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0019_auto_20201222_0715"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beneficialowner",
            name="verification_document_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("driver_license", "Driver’s License"),
                    ("us_passport", "US Passport"),
                    ("foreign_passport", "Foreign Passport"),
                    ("us_visa", "US Visa"),
                    (
                        "employment_authorization_card",
                        "Federal Employment Authorization Card",
                    ),
                ],
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="controllerdetails",
            name="verification_document_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("driver_license", "Driver’s License"),
                    ("us_passport", "US Passport"),
                    ("foreign_passport", "Foreign Passport"),
                    ("us_visa", "US Visa"),
                    (
                        "employment_authorization_card",
                        "Federal Employment Authorization Card",
                    ),
                ],
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="incorporationdetails",
            name="verification_document_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ein_letter", "EIN Letter"),
                    ("business_license", "Business License"),
                    ("driver_license", "Driver’s License"),
                    ("us_passport", "US Passport"),
                ],
                max_length=32,
            ),
        ),
    ]
