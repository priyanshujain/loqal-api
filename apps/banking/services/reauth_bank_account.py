from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.banking.dbapi import update_bank_account
from apps.banking.validators import ReauthBankAccountValidator
from plugins.plaid import PlaidPlugin


class ReAuthBankAccount(ServiceBase):
    def __init__(self, bank_account, data):
        self.bank_account = bank_account
        self.data = data

    def handle(self):
        data = self._validate_data()
        plaid_item = self._process_plaid_token(data=data)
        plaid_access_token = plaid_item["plaid_access_token"]
        plaid_account_id = self.bank_account.plaid_account_id

        self._update_bank_account(
            plaid_access_token=plaid_access_token,
            plaid_account_id=plaid_account_id,
        )
        self.bank_account.set_verified()

    def _process_plaid_token(self, data):
        plaid_public_token = data["plaid_public_token"]

        plaid = PlaidPlugin()
        access_token = plaid.exchange_public_token(
            public_token=plaid_public_token
        )
        if not access_token:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Invalid credentials/ bank account does not match.")
                    )
                }
            )
        return {
            "plaid_access_token": access_token,
        }

    def _validate_data(self):
        data = run_validator(
            validator=ReauthBankAccountValidator, data=self.data
        )
        return data

    def _update_bank_account(
        self,
        plaid_access_token,
        plaid_account_id,
    ):
        update_bank_account(
            bank_account_id=self.bank_account.id,
            plaid_access_token=plaid_access_token,
            plaid_account_id=plaid_account_id,
        )
