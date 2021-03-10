from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.fields.related import RelatedField
from django.utils import timezone

from apps.account.models import Account, MerchantAccount
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel

__all__ = (
    "PaymentRegister",
    "MerchantReceiveLimit",
)


class PaymentRegister(AbstractBaseModel):
    account = models.OneToOneField(Account, on_delete=models.DO_NOTHING)
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    daily_send_limit = models.DecimalField(
        max_digits=10,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=5000,
    )
    weekly_send_limit = models.DecimalField(
        max_digits=10,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=5000,
    )
    daily_usage = models.DecimalField(
        max_digits=10,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    daily_usage_start_time = models.DateTimeField(default=timezone.now)
    weekly_usage = models.DecimalField(
        max_digits=10,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    weekly_usage_start_time = models.DateTimeField(default=timezone.now)
    passcode_required_minimum = models.DecimalField(
        max_digits=10,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=100,
    )

    class Meta:
        db_table = "payment_register"

    def update_usage(self, amount, last_used_at):
        amount = Decimal(amount)
        if last_used_at >= self.daily_usage_start_time + timedelta(hours=24):
            self.daily_usage_start_time = last_used_at
            self.daily_usage = amount
        else:
            self.daily_usage += amount

        if last_used_at >= self.weekly_usage_start_time + timedelta(days=7):
            self.weekly_usage_start_time = last_used_at
            self.weekly_usage = amount
        else:
            self.weekly_usage += amount
        self.save()

    def set_daily_limit(self, value):
        self.daily_send_limit = Decimal(value)
        self.save()

    def set_weekly_limit(self, value):
        self.weekly_send_limit = Decimal(value)
        self.save()

    def set_passcode_threshold(self, value):
        self.passcode_required_minimum = Decimal(value)
        self.save()


class MerchantReceiveLimit(AbstractBaseModel):
    merchant = models.OneToOneField(
        MerchantAccount,
        on_delete=models.DO_NOTHING,
        related_name="receive_limit",
    )
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    transaction_limit = models.DecimalField(
        max_digits=10,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=500,
    )

    class Meta:
        db_table = "merchant_receive_limit"

    def update_limit(self, transaction_limit, save=True):
        self.transaction_limit = transaction_limit
        if save:
            self.save()
