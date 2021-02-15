from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.banking.dbapi import (create_bank_account_via_iav,
                                get_bank_account_by_dwolla_id)
from apps.banking.options import (DwollaFundingSourceStatus,
                                  MicroDepositStatus, VerificationType)
from apps.banking.validators import VerifyMicroDepositValidator
from apps.provider.lib.actions import ProviderAPIActionBase


class DwollaFundingSourceStatusMap:
    verified = DwollaFundingSourceStatus.VERIFIED
    unverified = DwollaFundingSourceStatus.UNVERIFIED


class SyncBankAccounts(ServiceBase):
    def __init__(self, account):
        self.account = account

    def handle(self):
        bank_accounts = GetAllBankAccountsAPIAction(
            account_id=self.account.id
        ).get()
        for bank_account in bank_accounts:
            links = bank_account["_links"]
            micro_deposit_verification_available = (
                "verify-micro-deposits" in links
            )
            is_micro_deposit = "micro-deposits" in links
            data = {
                "status": getattr(
                    DwollaFundingSourceStatusMap, bank_account["status"]
                ),
                "name": bank_account["name"],
                "bank_name": bank_account.get("bankName", ""),
                "dwolla_id": bank_account["id"],
                "removed": bank_account["removed"],
                "bank_account_type": bank_account["bankAccountType"],
                "micro_deposit_verification_available": micro_deposit_verification_available,
                "is_micro_deposit": is_micro_deposit,
            }
            existing_bank_account = get_bank_account_by_dwolla_id(
                dwolla_id=data["dwolla_id"]
            )
            if existing_bank_account:
                existing_bank_account.update_bank_account_from_sync(
                    dwolla_funding_source_status=data["status"],
                    is_dwolla_removed=data["removed"],
                )
            else:
                micro_deposit_status = MicroDepositStatus.NA
                if is_micro_deposit:
                    if data["status"] == DwollaFundingSourceStatus.VERIFIED:
                        micro_deposit_status = MicroDepositStatus.VERIFIED
                    else:
                        micro_deposit_status = MicroDepositStatus.PENDING
                create_bank_account_via_iav(
                    account_id=self.account.id,
                    bank_name=data["bank_name"],
                    bank_account_type=data["bank_account_type"],
                    name=data["name"],
                    status=data["status"],
                    dwolla_id=data["dwolla_id"],
                    verification_type=(
                        VerificationType.INSTANT
                        if is_micro_deposit
                        else VerificationType.MICRO_DEPOSIT
                    ),
                    micro_deposit_status=micro_deposit_status,
                )


class GetAllBankAccountsAPIAction(ProviderAPIActionBase):
    def get(self):
        response = self.client.banking.get_bank_accounts()
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": response.get(
                        "errors", "An unexpected error occurred."
                    )
                }
            )
        return response["data"]["bank_accounts"]
