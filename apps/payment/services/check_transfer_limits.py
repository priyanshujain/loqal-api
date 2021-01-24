from decimal import Decimal

from django.db.models import Sum
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from apps.payment.dbapi import (get_payment_register,
                                get_transactions_by_bank_account)
from apps.payment.models import payment_request

__all__ = ("CheckTransferLimit",)


class CheckTransferLimit(object):
    def __init__(self, bank_account, amount):
        self.bank_account = bank_account
        self.amount = Decimal(amount)

    def handle(self):
        payment_register = get_payment_register(
            account_id=self.bank_account.account.id
        )
        if not payment_request:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Payment register could not found. Please contact our support team."
                        )
                    )
                }
            )
        weekly_total = (
            get_transactions_by_bank_account(
                from_datetime=payment_register.weekly_usage_start_time,
                bank_account_id=self.bank_account.id,
            ).aggregate(total=Sum("amount"))["total"]
            + self.amount
        )

        daily_total = (
            get_transactions_by_bank_account(
                from_datetime=payment_register.daily_usage_start_time,
                bank_account_id=self.bank_account.id,
            ).aggregate(total=Sum("amount"))["total"]
            + self.amount
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
