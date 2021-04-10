from django.db import models

from apps.account.models import MerchantAccount
from db.models import AbstractBaseModel


class B2CInvite(AbstractBaseModel):
    consumer_name = models.CharField(max_length=256, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=10, default=None, null=True)
    phone_number_country = models.CharField(max_length=2, default="US")
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "b2c_invite"

    def set_used(self, save=True):
        self.is_used = True
        if save:
            self.save()


class B2BInvite(AbstractBaseModel):
    merchant_name = models.CharField(max_length=256, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=10, default=None, null=True)
    phone_number_country = models.CharField(max_length=2, default="US")
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "b2b_invite"
