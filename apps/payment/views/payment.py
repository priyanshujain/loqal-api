from api.views import ConsumerAPIView, MerchantAPIView
from apps.payment.dbapi import get_transactions, get_consumer_payment_reqeust, get_merchant_payment_reqeust
from apps.payment.responses import TransactionResponse, PaymentRequestResponse, ConsumerPaymentRequestResponse
from apps.payment.services import CreatePayment, CreatePaymentRequest


class CreatePaymentAPI(ConsumerAPIView):
    def post(self, request):
        account_id = request.account.id
        service_response = self._run_services(account_id=account_id)
        return self.response(
            TransactionResponse(service_response).data, status=201
        )

    def _run_services(self, account_id):
        return CreatePayment(
            account_id=account_id, data=self.request_data
        ).handle()


class PaymentHistoryAPI(ConsumerAPIView):
    def get(self, request):
        account_id = request.account.id
        transactions = get_transactions(account_id=account_id)
        return self.response(
            TransactionResponse(transactions, many=True).data, status=201
        )



class CreatePaymentRequestAPI(MerchantAPIView):
    def post(self, request):
        account_id = request.account.id
        payment_request = CreatePaymentRequest(account_id=account_id, data=self.request_data).handle()
        return self.response(PaymentRequestResponse(payment_request).data, status=201)



class ListMerchantPaymentRequestAPI(ConsumerAPIView):
    def post(self, request):
        account_id = request.account.id
        payment_requests = get_merchant_payment_reqeust(account_id=account_id)
        return self.response(PaymentRequestResponse(payment_requests).data, status=201)




class ListConsumerPaymentRequestAPI(ConsumerAPIView):
    def post(self, request):
        account_id = request.account.id
        payment_requests = get_consumer_payment_reqeust(account_id=account_id)
        return self.response(ConsumerPaymentRequestResponse(payment_requests).data, status=201)


