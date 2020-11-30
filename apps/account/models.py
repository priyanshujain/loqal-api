from django.db import models

from db.models.abstract import AbstractBase
from apps.user.models import User

__all__ = (
    "Account",
    "FeatureAccess",
    "AccountSettings",
)


class Account(AbstractBase):
    dwolla_correlation_id = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "account"


class ConsumerAccount(AbstractBase):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "consumer_account"


class MerchantAccount(AbstractBase):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=256)
    website = models.URLField(max_length=255, null=True, blank=True,)
    company_email = models.CharField(max_length=255)
    business_contact_number = models.CharField(max_length=20)

    class Meta:
        db_table = "account_settings"
