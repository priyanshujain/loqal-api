from decimal import Decimal

from django.conf import settings
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from apps.banking.dbapi import get_bank_account
from plugins.plaid import PlaidPlugin

__all__ = ("ValidateBankBalance",)


class ValidateBankBalance(object):
    def __init__(self, sender_account_id, receiver_account_id, total_amount):
        self.sender_account_id = sender_account_id
        self.receiver_account_id = receiver_account_id
        self.total_amount = total_amount

    def validate(self):
        sender_bank_account = get_bank_account(
            account_id=self.sender_account_id
        )

        if not sender_bank_account:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        "Please add the bank account before making payment."
                    )
                }
            )

        receiver_bank_account = get_bank_account(
            account_id=self.receiver_account_id
        )
        if not receiver_bank_account:
            raise ValidationError(
                {"detail": ErrorDetail("Receiver account is not active yet.")}
            )

        balance = self._check_balance(bank_account=sender_bank_account)
        min_required_balance = self.total_amount + Decimal(
            settings.MIN_BANK_ACCOUNT_BALANCE_REQUIRED
        )
        if balance < min_required_balance:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        "You need minimum $100 excess of given amount to make a payment."
                    )
                }
            )
        return {
            "sender_bank_account": sender_bank_account,
            "receiver_bank_account": receiver_bank_account,
            "sender_bank_balance": balance,
        }

    def _check_balance(self, bank_account):
        plaid = PlaidPlugin()
        balance = plaid.get_balance(
            access_token=bank_account.plaid_access_token,
            account_id=bank_account.plaid_account_id,
        )
        if not balance:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Balance check failed, please try again.")
                    )
                }
            )
        return balance
