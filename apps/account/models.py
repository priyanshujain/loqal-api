from django.db import models
from django.utils.translation import gettext as _
from apps.user.models import User
from db.models.abstract import AbstractBaseModel
from utils.shortcuts import generate_uuid_hex
from db.models.fields import ChoiceEnumField
from apps.account.options import MerchantAccountStatus


__all__ = (
    "Account",
    "FeatureAccess",
    "AccountSettings",
)


class Account(AbstractBaseModel):
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


class ConsumerAccount(AbstractBaseModel):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "account",
            "user",
        )
        db_table = "consumer_account"


class MerchantAccount(AbstractBaseModel):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=256)
    company_email = models.CharField(max_length=255)
    account_status = ChoiceEnumField(
        enum_type=MerchantAccountStatus,
        default=MerchantAccountStatus.PENDING,
        help_text=_("Status for the merchant account with dwolla."),
    )

    class Meta:
        db_table = "account_settings"
