from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from apps.banking.dbapi import get_bank_account
from apps.banking.options import PlaidBankAccountStatus

__all__ = ("ValidateBankAccount",)


class ValidateBankAccount(object):
    def __init__(self, sender_account_id, receiver_account_id):
        self.sender_account_id = sender_account_id
        self.receiver_account_id = receiver_account_id

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

        if sender_bank_account.plaid_status != PlaidBankAccountStatus.VERIFIED:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        "Bank account is not verified, please verify your bank account."
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

        return {
            "sender_bank_account": sender_bank_account,
            "receiver_bank_account": receiver_bank_account,
        }
