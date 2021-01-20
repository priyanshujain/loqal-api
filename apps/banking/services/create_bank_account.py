from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.banking.dbapi import create_bank_account
from apps.banking.validators import CreateBankAccountValidator
from apps.provider.lib.actions import ProviderAPIActionBase
from plugins.plaid import PlaidPlugin


class CreateBankAccount(ServiceBase):
    def __init__(self, account_id, data):
        self.account_id = account_id
        self.data = data

    def handle(self):
        data = self._validate_data()
        plaid_item = self._process_plaid_token(data=data)
        plaid_access_token = plaid_item["plaid_access_token"]
        plaid_account_id = data["plaid_account_id"]
        account_number_suffix = plaid_item["bank_account"].get(
            "account_number", ""
        )[-4:]
        bank_name = plaid_item["bank_account"]["institution"].get("name")
        account_name = plaid_item["bank_account"].get("name")
        bank_logo_base64 = plaid_item["bank_account"]["institution"].get(
            "logo_base64"
        )

        bank_account = self._factory_bank_account(
            plaid_access_token=plaid_access_token,
            plaid_account_id=plaid_account_id,
            account_number_suffix=account_number_suffix,
            bank_name=bank_name,
            bank_logo_base64=bank_logo_base64,
            name=account_name,
        )
        bank_account.set_plaid_verified()

        plaid_processor_token = plaid_item["plaid_processor_token"]
        dwolla_account_data = self._send_to_dwolla(
            processor_token=plaid_processor_token, account_name=account_name
        )
        dwolla_funding_source_id = dwolla_account_data[
            "dwolla_funding_source_id"
        ]
        bank_account.add_dwolla_id(dwolla_id=dwolla_funding_source_id)
        return bank_account

    def _validate_data(self):
        return run_validator(
            validator=CreateBankAccountValidator, data=self.data
        )

    def _process_plaid_token(self, data):
        plaid_public_token = data["plaid_public_token"]
        plaid_account_id = data["plaid_account_id"]

        plaid = PlaidPlugin()
        access_token = plaid.exchange_public_token(
            public_token=plaid_public_token
        )
        if not access_token:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("plaid_public_token has been expired.")
                    )
                }
            )
        bank_account = plaid.get_bank_account(
            access_token=access_token, account_id=plaid_account_id
        )
        if not bank_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("plaid_account_id is not valid."))}
            )
        processor_token = plaid.get_dwolla_processor_token(
            access_token=access_token, account_id=plaid_account_id
        )
        return {
            "plaid_access_token": access_token,
            "plaid_processor_token": processor_token,
            "bank_account": bank_account,
        }

    def _factory_bank_account(
        self,
        plaid_access_token,
        plaid_account_id,
        account_number_suffix,
        bank_name,
        bank_logo_base64,
        name,
    ):
        bank_account = create_bank_account(
            account_id=self.account_id,
            plaid_access_token=plaid_access_token,
            plaid_account_id=plaid_account_id,
            account_number_suffix=account_number_suffix,
            bank_name=bank_name,
            bank_logo_base64=bank_logo_base64,
            name=name,
        )
        return bank_account

    def _send_to_dwolla(self, processor_token, account_name):
        api_action = CreateBankAccountAPIAction(account_id=self.account_id)
        account_data = api_action.create(
            data={
                "processor_token": processor_token,
                "account_name": account_name,
            }
        )
        return account_data


class CreateBankAccountAPIAction(ProviderAPIActionBase):
    def create(self, data):
        response = self.client.banking.create_bank_account(data=data)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return {
            "status": response["data"].get("status"),
            "dwolla_funding_source_id": response["data"][
                "dwolla_funding_source_id"
            ],
        }
