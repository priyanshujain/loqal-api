from api.views import UserAPIView
from apps.banking.response import BankAccountResponse
from apps.banking.services import CreateBankAccount


class CreateBankAccountAPI(UserAPIView):
    def post(self, request):
        account = request.account
        bank_account = self._run_services(account_id=account.id)
        return self.response(
            BankAccountResponse(bank_account).data, status=201
        )

    def _run_services(self, account_id):
        service = CreateBankAccount(
            account_id=account_id, data=self.request_data
        )
        return service.execute()
