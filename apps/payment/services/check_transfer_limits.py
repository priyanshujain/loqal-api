from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from apps.payment.dbapi import get_transactions_by_bank_account

__all__ = ("CheckTransferLimit",)


class CheckTransferLimit(object):
    def __init__(self, register, bank_account, amount):
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
        daily_total = (
            get_transactions_by_bank_account(
                from_datetime=payment_register.daily_usage_start_time,
                bank_account_id=self.bank_account.id,
            ).aggregate(total=Sum("amount"))["total"]
            or Decimal(0.0) + self.amount
        )
        if daily_total > payment_register.daily_send_limit:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "You have reached the Loqal payment limit($500/day). "
                            "Please try again after 24 hours."
                        )
                    ),
                    "code": "DAILY_LIMIT_EXCEEDED",
                }
            )

    def _check_weekly_limit(self):
        payment_register = self.register
        weekly_total = (
            get_transactions_by_bank_account(
                from_datetime=payment_register.weekly_usage_start_time,
                bank_account_id=self.bank_account.id,
            ).aggregate(total=Sum("amount"))["total"]
            or Decimal(0.0) + self.amount
        )
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
