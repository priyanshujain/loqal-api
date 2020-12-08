from django.db import models

from apps.user.models import User
from db.models.abstract import AbstractBase
from utils.shortcuts import generate_uuid_hex

__all__ = (
    "Account",
    "FeatureAccess",
    "AccountSettings",
)


class Account(AbstractBase):
    dwolla_correlation_id = models.CharField(
        max_length=40, default=generate_uuid_hex, editable=False, unique=True
    )
    dwolla_id = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    zip_code = models.CharField(max_length=5, blank=True)

    def add_dwolla_id(self, dwolla_id):
        """
        docstring
        """
        self.dwolla_id = dwolla_id
        self.save()

    def add_zip_code(self, zip_code):
        """
        docstring
        """
        self.zip_code = zip_code
        self.save()

    class Meta:
        db_table = "account"


class ConsumerAccount(AbstractBase):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "account",
            "user",
        )
        db_table = "consumer_account"


class MerchantAccount(AbstractBase):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=256)
    website = models.URLField(max_length=255, null=True, blank=True,)
    company_email = models.CharField(max_length=255)
    business_contact_number = models.CharField(max_length=20)

    class Meta:
        db_table = "account_settings"
