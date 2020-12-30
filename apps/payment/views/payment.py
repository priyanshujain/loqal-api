from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView, MerchantAPIView
from apps.payment.dbapi import (get_consumer_payment_reqeust,
                                get_consumer_transaction,
                                get_consumer_transactions,
                                get_merchant_payment_reqeust)
from apps.payment.models import transaction
from apps.payment.responses import (ConsumerPaymentRequestResponse,
                                    PaymentRequestResponse,
                                    TransactionDetailsResponse,
                                    TransactionHistoryResponse,
                                    TransactionResponse)
from apps.payment.services import (ApprovePaymentRequest, CreatePaymentRequest,
                                   CreateRefund, DirectMerchantPayment,
                                   RejectPaymentRequest)


class CreatePaymentAPI(ConsumerAPIView):
    def post(self, request):
        consumer_account = request.consumer_account
        merchant_payment = DirectMerchantPayment(
            consumer_account=consumer_account,
            data=self.request_data,
            ip_address=request.ip,
        ).handle()
        transaction_data = TransactionResponse(
            merchant_payment.transaction
        ).data
        transaction_data["tip_amount"] = merchant_payment.tip_amount
        return self.response(transaction_data, status=201)


class PaymentHistoryAPI(ConsumerAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        transactions = get_consumer_transactions(
            consumer_account=consumer_account
        )
        return self.response(
            TransactionHistoryResponse(transactions, many=True).data
        )


class TransactionDetailsAPI(ConsumerAPIView):
    def get(self, request, transaction_id):
        consumer_account = request.consumer_account
        transaction = get_consumer_transaction(
            consumer_account=consumer_account,
            transaction_tracking_id=transaction_id,
        )
        if not transaction:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid transaction_id."))}
            )
        return self.response(TransactionDetailsResponse(transaction).data)


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
