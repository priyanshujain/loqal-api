from api.views import ConsumerAPIView
from apps.banking.dbapi import get_bank_account
from apps.banking.response import BankAccountResponse
from apps.banking.services import CreateBankAccount, PlaidLink


class CreateBankAccountAPI(ConsumerAPIView):
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


class GetBankAccountAPI(ConsumerAPIView):
    def get(self, request):
        account = request.account
        bank_account = get_bank_account(account_id=account.id)
        if bank_account:
            return self.response(BankAccountResponse(bank_account).data)
        return self.response()


class PlaidLinkTokenAPI(ConsumerAPIView):
    def get(self, request):
        account = request.account
        token = PlaidLink(account_uid=account.u_id.hex).token
        return self.response({"token": token})
