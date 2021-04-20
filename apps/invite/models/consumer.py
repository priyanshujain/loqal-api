from django.db import models

from apps.account.models import ConsumerAccount
from db.models import AbstractBaseModel


class C2CInvite(AbstractBaseModel):
    phone_number = models.CharField(max_length=10, default=None, null=True)
    phone_number_country = models.CharField(max_length=2, default="US")
    consumer_name = models.CharField(max_length=256, blank=True)
    email = models.EmailField(blank=True)
    consumer = models.ForeignKey(ConsumerAccount, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "c2c_invite"

    def set_used(self, save=True):
        self.is_used = True
        if save:
            self.save()


class C2BInvite(AbstractBaseModel):
    phone_number = models.CharField(max_length=10, default=None, null=True)
    phone_number_country = models.CharField(max_length=2, default="US")
    merchant_name = models.CharField(max_length=256, blank=True)
    email = models.EmailField(blank=True)
    consumer = models.ForeignKey(ConsumerAccount, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "c2b_invite"
