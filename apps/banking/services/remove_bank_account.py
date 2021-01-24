from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.banking.dbapi import get_bank_account
from apps.provider.lib.actions import ProviderAPIActionBase

__all__ = ("RemoveBankAccount",)


class RemoveBankAccount(ServiceBase):
    def __init__(self, account_id):
        self.account_id = account_id

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
        response = BankAccountAPIAction().remove(
            dwolla_id=bank_account.dwolla_id
        )
        if response["is_success"] == True:
            bank_account.set_dwolla_removed()
        return True


class BankAccountAPIAction(ProviderAPIActionBase):
    def remove(self, dwolla_id):
        response = self.client.banking.remove_bank_account(
            funding_source_id=dwolla_id
        )
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
