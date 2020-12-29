from django.conf import settings
from django.db import models

from apps.merchant.models import AccountMember
from db.models import AbstractBaseModel

from .payment import Payment
from .qrcode import PaymentQrCode
from .transaction import Transaction

__all__ = ("DirectMerchantPayment",)


class DirectMerchantPayment(AbstractBaseModel):
    payment_qrcode = models.ForeignKey(
        PaymentQrCode,
        blank=True,
        null=True,
        related_name="direct_merchant_payments",
        on_delete=models.SET_NULL,
    )
    cashier = models.ForeignKey(
        AccountMember,
        blank=True,
        null=True,
        related_name="direct_merchant_payments",
        on_delete=models.SET_NULL,
    )
    tip_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    payment = models.ForeignKey(
        Payment,
        blank=True,
        null=True,
        related_name="direct_merchant_payments",
        on_delete=models.SET_NULL,
    )
    transaction = models.OneToOneField(
        Transaction,
        blank=True,
        null=True,
        related_name="direct_merchant_payments",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "direct_merchant_payment"

    def add_transaction(self, transaction, save=True):
        self.transaction = transaction
        if save:
            self.save()
