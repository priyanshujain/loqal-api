from rest_framework.exceptions import ErrorDetail
from api.views import ConsumerAPIView, MerchantAPIView
from apps.payment.dbapi import (get_consumer_payment_reqeust,
                                get_merchant_payment_reqeust, get_transactions,
                                get_transactions_to_merchant,
                                get_customers_aggregate_transactions)
from apps.payment.responses import (ConsumerPaymentRequestResponse,
                                    PaymentRequestResponse,
                                    TransactionResponse,
                                    MerchantTransactionResponse)
from apps.payment.services import (ApprovePaymentRequest, CreatePayment,
                                   CreatePaymentRequest, RejectPaymentRequest)
from api.utils.dates import get_date_range_from_params, InvalidParams
from api.exceptions import ValidationError, ErrorDetail
from django.utils.translation import gettext as _


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
        return self.response(TransactionResponse(transactions, many=True).data)


class CreatePaymentRequestAPI(MerchantAPIView):
    def post(self, request):
        account_id = request.account.id
        payment_request = CreatePaymentRequest(
            account_id=account_id, data=self.request_data
        ).handle()
        return self.response(
            PaymentRequestResponse(payment_request).data, status=201
        )


class ApprovePaymentRequestAPI(ConsumerAPIView):
    def post(self, request):
        account_id = request.account.id
        transaction = ApprovePaymentRequest(
            account_id=account_id, data=self.request_data
        ).handle()
        return self.response(TransactionResponse(transaction).data)


class RejectPaymentRequestAPI(ConsumerAPIView):
    def post(self, request):
        account_id = request.account.id
        RejectPaymentRequest(
            account_id=account_id, data=self.request_data
        ).handle()
        return self.response()


class ListMerchantPaymentRequestAPI(MerchantAPIView):
    def get(self, request):
        account_id = request.account.id
        payment_requests = get_merchant_payment_reqeust(account_id=account_id)
        return self.response(
            PaymentRequestResponse(payment_requests, many=True).data
        )


class ListConsumerPaymentRequestAPI(ConsumerAPIView):
    def get(self, request):
        account_id = request.account.id
        payment_requests = get_consumer_payment_reqeust(account_id=account_id)
        return self.response(
            ConsumerPaymentRequestResponse(payment_requests, many=True).data
        )


class MerchantPaymentHistoryAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        start, end = self.validate_params(params=self.request_data)
        transactions = get_transactions_to_merchant(account_id=merchant_account.account.id)
        
        if start and end:
            transactions = transactions.filter(created_at__range=[start, end])
        return self.response(MerchantTransactionResponse(transactions, many=True).data)
    
    def validate_params(self, params):
        try:
            start, end = get_date_range_from_params(params=params, optional=True)
        except InvalidParams as e:
            raise ValidationError({
                "detail": ErrorDetail(_(str(e)))
            })
        return start, end


class CustomersAggregateHistoryAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        customers = get_customers_aggregate_transactions(account_id=merchant_account.account.id)
        data = []
        # for customer in customers:
        #     data.append({
        #         "first_name": customer["first_name"],
        #         "total": customer["total"]
        #     })
        return self.response(customers)