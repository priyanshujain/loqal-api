from django.utils.translation import gettext as _
from django.db.models import Sum

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.banking.dbapi import get_bank_account
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.payment.dbapi import (
    get_pending_transactions_merchant,
    get_pending_transactions_sender,
    empty_transactions,
)

__all__ = ("RemoveBankAccount",)


class RemoveBankAccount(ServiceBase):
    def __init__(self, account_id, is_merchant=False):
        self.account_id = account_id
        self.is_merchant = is_merchant

    def handle(self):
        bank_account = get_bank_account(account_id=self.account_id)
        if not bank_account:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Bank account does does exist for your account.")
                    )
                }
            )

        transactions = empty_transactions()
        if self.is_merchant:
            transactions = get_pending_transactions_merchant(
                bank_account_id=bank_account.id
            )
        else:
            transactions = get_pending_transactions_sender(
                bank_account_id=bank_account.id
            )

        pending_amount = transactions.aggregate(total=Sum("amount"))["total"]
        if pending_amount > 0:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            f"You have pending transctions worth ${pending_amount}"
                            ". Please wait until these transactions are "
                            "processed before removing your account."
                        )
                    )
                }
            )

        response = BankAccountAPIAction().remove(dwolla_id=bank_account.dwolla_id)
        if response["is_success"] == True:
            bank_account.set_dwolla_removed()
        return True


class BankAccountAPIAction(ProviderAPIActionBase):
    def remove(self, dwolla_id):
        response = self.client.banking.remove_bank_account(funding_source_id=dwolla_id)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service is facing a technical issue, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return response["data"]
