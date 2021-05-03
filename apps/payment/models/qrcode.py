from django.db import models

from apps.account.models import MerchantAccount
from apps.merchant.models import AccountMember
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel

__all__ = ("PaymentQrCode",)


class PaymentQrCode(AbstractBaseModel):
    merchant = models.ForeignKey(
        MerchantAccount, on_delete=models.CASCADE, blank=True, null=True
    )
    cashier = models.ForeignKey(
        AccountMember, on_delete=models.SET_NULL, blank=True, null=True
    )
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    qrcode_id = models.CharField(max_length=10, unique=True)
    register_name = models.CharField(max_length=255, blank=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        db_table = "payment_qrcode"
        unique_together = (
            "merchant",
            "cashier",
        )
