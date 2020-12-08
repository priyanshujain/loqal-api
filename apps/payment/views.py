from api.views import UserAPIView
from apps.payment.services import CreatePayment
from apps.payment.responses import TransactionResponse


class CreatePaymentAPI(UserAPIView):
    def post(self, request):
        account_id = request.account.id
        service_response = self._run_services(account_id=account_id)
        return self.response(TransactionResponse(service_response), status=201)

    def _run_services(self, account_id):
        return CreatePayment(
            account_id=account_id, data=self.request_data
        ).execute()

