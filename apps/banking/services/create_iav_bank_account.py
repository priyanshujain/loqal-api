from uuid import UUID

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.banking.dbapi import create_bank_account_via_iav
from apps.banking.notifications import SendVerifyMicroDepositEmail
from apps.banking.options import MicroDepositStatus, VerificationType
from apps.banking.validators import CreateIAVBankAccountValidator
from apps.provider.lib.actions import ProviderAPIActionBase


class CreateIAVBankAccount(ServiceBase):
    def __init__(self, account, data, user):
        self.account = account
        self.data = data
        self.user = user

    def handle(self):
        dwolla_id = self._validate_data()
        data = GetBankAccountAPIAction(account_id=self.account.id).get(
            dwolla_id=dwolla_id
        )
        customer_dwolla_id = data["customer_dwolla_id"]
        if self.account.dwolla_id != customer_dwolla_id:
            raise ValidationError(
                {"detail": ErrorDetail(_("Funding source is not valid."))}
            )

        micro_deposit_verification_available = data[
            "micro_deposit_verification_available"
        ]
        is_micro_deposit = data["is_micro_deposit"]
        verification_type = VerificationType.INSTANT
        micro_deposit_status = MicroDepositStatus.NA

        if is_micro_deposit:
            verification_type = VerificationType.MICRO_DEPOSIT
            micro_deposit_status = MicroDepositStatus.PENDING

        if micro_deposit_verification_available:
            micro_deposit_status = MicroDepositStatus.AWAITING_VERIFICATION

        bank_account = self._factory_bank_account(
            status=data["status"],
            bank_name=data["bank_name"],
            dwolla_id=data["dwolla_id"],
            name=data["name"],
            bank_account_type=data["bank_account_type"],
            verification_type=verification_type,
            micro_deposit_status=micro_deposit_status,
        )
        if micro_deposit_verification_available:
            SendVerifyMicroDepositEmail(email=self.user.email).send()

        return bank_account

    def _validate_data(self):
        data = run_validator(
            validator=CreateIAVBankAccountValidator, data=self.data
        )
        funding_source_url = data["funding_source_url"]
        try:
            dwolla_id = funding_source_url.split("/").pop()
            dwolla_id_uuid = UUID(dwolla_id, version=4)
            return dwolla_id
        except ValueError:
            raise ValidationError(
                {"detail": ErrorDetail(_("Funding source URL is not valid."))}
            )

    def _factory_bank_account(
        self,
        status,
        bank_name,
        dwolla_id,
        name,
        bank_account_type,
        verification_type,
        micro_deposit_status,
    ):
        bank_account = create_bank_account_via_iav(
            account_id=self.account.id,
            bank_name=bank_name,
            name=name,
            status=status,
            dwolla_id=dwolla_id,
            bank_account_type=bank_account_type,
            verification_type=verification_type,
            micro_deposit_status=micro_deposit_status,
        )
        return bank_account


class GetBankAccountAPIAction(ProviderAPIActionBase):
    def get(self, dwolla_id):
        response = self.client.banking.get_bank_account(
            funding_source_id=dwolla_id
        )
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "message": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    ),
                    "detail": ErrorDetail(
                        _(
                            "Your bank account couldn't be added, Please try "
                            "again later. If the problem persists, please "
                            "contact our support team."
                        )
                    ),
                }
            )
        return response["data"]
