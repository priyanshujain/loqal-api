from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from apps.merchant.services.profile import merchant_profile
from apps.payment.dbapi import get_merchant_receive_limit

__all__ = ("CheckTransferLimit",)


class CheckTransferLimit(object):
    def __init__(self, merchant, register, bank_account, amount):
        self.merchant = merchant
        self.register = register
        self.bank_account = bank_account
        self.amount = Decimal(amount)

    def handle(self):
        payment_register = self.register
        if not payment_register:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Payment register could not found. Please contact our support team."
                        )
                    )
                }
            )
        merchant_receive_limit = get_merchant_receive_limit(
            merchant_id=self.merchant.id
        )
        if merchant_receive_limit:
            self._check_merchant_receive_limit(merchant_receive_limit)
        current_time = timezone.now()
        if current_time < payment_register.daily_usage_start_time + timedelta(
            hours=24
        ):
            self._check_daily_limit()

        if (
            current_time
            < payment_register.weekly_usage_start_time + timedelta(days=7)
        ):
            self._check_weekly_limit()

    def _check_daily_limit(self):
        payment_register = self.register
        daily_total = payment_register.daily_usage + self.amount
        if daily_total > payment_register.daily_send_limit:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            f"You have reached the Loqal payment limit(${payment_register.daily_send_limit}/day). "
                            "Please try again after 24 hours."
                        )
                    ),
                    "code": "DAILY_LIMIT_EXCEEDED",
                }
            )

    def _check_weekly_limit(self):
        payment_register = self.register
        weekly_total = payment_register.weekly_usage + self.amount
        if weekly_total > payment_register.weekly_send_limit:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "You have reached the Loqal payment limit($5000/week). "
                            "Please try again after 24 hours."
                        )
                    ),
                    "code": "WEEKLY_LIMIT_EXCEEDED",
                }
            )

    def _check_merchant_receive_limit(self, merchant_receive_limit):
        if self.amount > merchant_receive_limit.transaction_limit:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            f"The maximum transaction size to {self.merchant.profile.full_name}"
                            f" is {merchant_receive_limit.transaction_size}. Please contact the store for further details."
                        )
                    ),
                    "code": "MERCHANT_RECEIVE_LIMIT_EXCEEDED",
                }
            )
