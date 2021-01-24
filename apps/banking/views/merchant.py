import re

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import MerchantAPIView
from apps.banking.dbapi import get_bank_account
from apps.banking.options import BankAccountStatus
from apps.banking.response import BankAccountResponse
from apps.banking.services import (CreateBankAccount, PlaidLink,
                                   ReAuthBankAccount, RemoveBankAccount)


class CreateBankAccountAPI(MerchantAPIView):
    # TODO: add permission classes
    permission_classes = ()

    def post(self, request):
        account = request.account
        bank_account = get_bank_account(account_id=account.id)
        if bank_account:
            return self.response(BankAccountResponse(bank_account).data)

        bank_account = self._run_services(account_id=account.id)
        return self.response(
            BankAccountResponse(bank_account).data, status=201
        )

    def _run_services(self, account_id):
        service = CreateBankAccount(
            account_id=account_id, data=self.request_data
        )
        return service.handle()


class RemoveBankAccountAPI(MerchantAPIView):
    def post(self, request):
        account = request.account
        RemoveBankAccount(account_id=account.id).handle()
        return self.response()


class GetBankAccountAPI(MerchantAPIView):
    def get(self, request):
        account = request.account
        bank_account = get_bank_account(account_id=account.id)
        if bank_account:
            return self.response(BankAccountResponse(bank_account).data)
        return self.response()


class PlaidLinkTokenAPI(MerchantAPIView):
    def get(self, request):
        account = request.account
        bank_account = get_bank_account(account_id=account.id)
        if bank_account and bank_account.plaid_access_token:
            token = PlaidLink(
                account_uid=account.u_id.hex,
                access_token=bank_account.plaid_access_token,
            ).token
        else:
            token = PlaidLink(account_uid=account.u_id.hex).token
        return self.response({"token": token})


class ReAuthBankAccountAPI(MerchantAPIView):
    def post(self, request):
        account = request.account
        bank_account = get_bank_account(account_id=account.id)
        if not bank_account:
            raise ValidationError(
                {"detail": ErrorDetail("Bank account does not exist.")}
            )

        if bank_account.plaid_status == BankAccountStatus.VERIFIED:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        "Bank account has already been verified."
                    )
                }
            )

        bank_account = ReAuthBankAccount(
            bank_account=bank_account, data=self.request_data
        ).handle()
        return self.response()
