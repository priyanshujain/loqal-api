from django.utils.translation import gettext as _
from rest_framework.exceptions import ErrorDetail

from api.exceptions import ErrorDetail, ValidationError
from api.utils.dates import InvalidParams, get_date_range_from_params
from api.views import ConsumerAPIView, MerchantAPIView
from apps.payment.dbapi import (get_consumer_payment_reqeust,
                                get_customers_aggregate_transactions,
                                get_merchant_payment_reqeust,
                                get_consumer_transactions,
                                get_transactions_to_merchant)
from apps.payment.responses import (ConsumerPaymentRequestResponse,
                                    MerchantTransactionResponse,
                                    PaymentRequestResponse, PaymentResponse,
                                    TransactionResponse,
                                    TransactionHistoryResponse,
                                    MerchantPaymentResponse,
                                    RefundPaymentResponse)
from apps.payment.services import (ApprovePaymentRequest, CreatePaymentRequest,
                                   DirectMerchantPayment, RejectPaymentRequest,
                                   CreateRefund,)


class CreatePaymentAPI(ConsumerAPIView):
    def post(self, request):
        consumer_account = request.consumer_account
        merchant_payment = DirectMerchantPayment(
            consumer_account=consumer_account,
            data=self.request_data,
            ip_address=request.ip,
        ).handle()
        return self.response(
            TransactionResponse(merchant_payment.transaction).data, status=201
        )


class PaymentHistoryAPI(ConsumerAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        transactions = get_consumer_transactions(consumer_account=consumer_account)
        return self.response(TransactionHistoryResponse(transactions, many=True).data)


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
            account_id=account_id,
            data=self.request_data,
            ip_address=request.ip,
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
        transactions = get_transactions_to_merchant(
            account_id=merchant_account.account.id
        )

        if start and end:
            transactions = transactions.filter(created_at__range=[start, end])
        return self.response(
            MerchantTransactionResponse(transactions, many=True).data
        )

    def validate_params(self, params):
        try:
            start, end = get_date_range_from_params(
                params=params, optional=True
            )
        except InvalidParams as e:
            raise ValidationError({"detail": ErrorDetail(_(str(e)))})
        return start, end


class CustomersAggregateHistoryAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        customers = get_customers_aggregate_transactions(
            account_id=merchant_account.account.id
        )
        return self.response(customers)


class CreateRefundPaymentAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        refund_payment = CreateRefund(
            merchant_account=merchant_account,
            data=self.request_data,
            ip_address=request.ip,
        ).handle()
        return self.response(
            TransactionResponse(refund_payment.transaction).data, status=201
        )
