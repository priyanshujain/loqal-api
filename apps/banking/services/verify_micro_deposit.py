from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.banking.dbapi import get_bank_account
from apps.banking.options import MicroDepositStatus
from apps.banking.validators import VerifyMicroDepositValidator
from apps.provider.lib.actions import ProviderAPIActionBase


class VerifyMicroDeposit(ServiceBase):
    def __init__(self, account, data):
        self.account = account
        self.data = data

    def handle(self):
        data = self._validate_data()
        bank_account = data["bank_account"]
        response = VerifyMicroDepositAPIAction().verify(
            data={
                "dwolla_id": bank_account.dwolla_id,
                "currency": bank_account.currency,
                "amount1": data["amount1"],
                "amount2": data["amount2"],
            }
        )
        bank_account.set_micro_deposit_verified(save=False)
        bank_account.update_dwolla_status(status=response["status"])
        return bank_account

    def _validate_data(self):
        data = run_validator(
            validator=VerifyMicroDepositValidator, data=self.data
        )
        bank_account = get_bank_account(account_id=self.account.id)
        if (
            bank_account.micro_deposit_status
            != MicroDepositStatus.AWAITING_VERIFICATION
        ):
            raise ValidationError(
                {"detail": ErrorDetail(_("Verification is not required."))}
            )
        if bank_account.max_attempts_exceeded:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "You have exceeded maximum attempts for bank "
                            "account verification. Please remove this bank "
                            "account and try again."
                        )
                    )
                }
            )
        data["bank_account"] = bank_account
        return data


class VerifyMicroDepositAPIAction(ProviderAPIActionBase):
    def verify(self, data):
        response = self.client.banking.verify_micro_deposit(data=data)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": response.get(
                        "errors", "An unexpected error occurred."
                    )
                }
            )
        return response["data"]
