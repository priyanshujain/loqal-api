from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView, MerchantAPIView
from apps.payment.dbapi import (get_consumer_payment_reqeust,
                                get_consumer_transaction,
                                get_consumer_transactions,
                                get_merchant_payment_reqeust,
                                get_recent_store_orders)
from apps.payment.notifications import (SendApproveRequestNotification,
                                        SendNewPaymentNotification,
                                        SendNewPaymentRequestNotification,
                                        SendRefundNotification,
                                        SendRejectRequestNotification)
from apps.payment.notifications.email import (RefundReceivedEmail,
                                              SendPaymentInitiatedEmail)
from apps.payment.responses import (ConsumerPaymentRequestResponse,
                                    DirectMerchantPaymentConsumerResponse,
                                    DirectMerchantPaymentResponse,
                                    MerchantTransactionHistoryResponse,
                                    PaymentRequestResponse,
                                    RecentStoresResponse,
                                    RefundHistoryResponse,
                                    TransactionDetailsResponse,
                                    TransactionHistoryResponse)
from apps.payment.services import (ApprovePaymentRequest, CreatePaymentRequest,
                                   CreateRefund, DirectMerchantPayment,
                                   RejectPaymentRequest)
from apps.rewards.services import AllocateRewards


class CreatePaymentAPI(ConsumerAPIView):
    def post(self, request):
        consumer_account = request.consumer_account
        merchant_payment = DirectMerchantPayment(
            consumer_account=consumer_account,
            data=self.request_data,
            ip_address=request.ip,
        ).handle()
        transaction_data = {}
        if merchant_payment.transaction:
            transaction_data = TransactionHistoryResponse(
                merchant_payment.transaction
            ).data
        else:
            transaction_data = DirectMerchantPaymentConsumerResponse(
                merchant_payment.payment
            ).data
        transaction_data["discount"] = {
            "amount": merchant_payment.payment.order.discount_amount,
            "name": merchant_payment.payment.order.discount_name,
        }
        transaction_data["tip_amount"] = merchant_payment.tip_amount
        payment_notification_data = {}
        if merchant_payment.transaction:
            payment_notification_data = MerchantTransactionHistoryResponse(
                merchant_payment.transaction
            ).data
        else:
            payment_notification_data = DirectMerchantPaymentResponse(
                merchant_payment.payment
            ).data
        payment_notification_data["tip_amount"] = str(
            merchant_payment.tip_amount
        )
        try:
            messsage = AllocateRewards(
                payment=merchant_payment.payment
            ).handle()
            if messsage:
                transaction_data["reward"] = messsage
        except Exception:
            pass
        SendNewPaymentNotification(
            merchant_id=merchant_payment.payment.order.merchant.id,
            data=payment_notification_data,
        ).send()
        if merchant_payment.transaction:
            SendPaymentInitiatedEmail(
                transaction=merchant_payment.transaction
            ).send()
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
        SendNewPaymentRequestNotification(
            user_id=payment_request.account_to.consumer.user.id,
            data=ConsumerPaymentRequestResponse(payment_request).data,
        ).send()
        return self.response(
            PaymentRequestResponse(payment_request).data, status=201
        )


class ApprovePaymentRequestAPI(ConsumerAPIView):
    def post(self, request):
        account_id = request.account.id
        payment_request = ApprovePaymentRequest(
            account_id=account_id,
            data=self.request_data,
            ip_address=request.ip,
        ).handle()
        transaction_data = TransactionHistoryResponse(
            payment_request.transaction
        ).data
        transaction_data["tip_amount"] = payment_request.tip_amount
        payment_notification_data = MerchantTransactionHistoryResponse(
            payment_request.transaction
        ).data
        payment_notification_data["tip_amount"] = str(
            payment_request.tip_amount
        )
        SendNewPaymentNotification(
            merchant_id=payment_request.payment.order.merchant.id,
            data=payment_notification_data,
        ).send()
        try:
            messsage = AllocateRewards(
                payment=payment_request.payment
            ).handle()
            if messsage:
                transaction_data["reward"] = messsage
        except Exception:
            pass
        SendApproveRequestNotification(
            merchant_id=payment_request.payment.order.merchant.id,
            data={
                "payment_request_id": str(payment_request.u_id),
                "payment_id": payment_request.payment.payment_tracking_id,
            },
        ).send()
        SendPaymentInitiatedEmail(
            transaction=payment_request.transaction
        ).send()
        return self.response(transaction_data)


class RejectPaymentRequestAPI(ConsumerAPIView):
    def post(self, request):
        account_id = request.account.id
        payment_request = RejectPaymentRequest(
            account_id=account_id, data=self.request_data
        ).handle()
        SendRejectRequestNotification(
            merchant_id=payment_request.payment.order.merchant.id,
            data={
                "payment_request_id": str(payment_request.u_id),
                "payment_id": payment_request.payment.payment_tracking_id,
            },
        ).send()
        return self.response()


class ListMerchantPaymentRequestAPI(MerchantAPIView):
    def get(self, request):
        account_id = request.account.id
        pending = self.request_data.get("pending")
        is_pending = False
        if pending == "true":
            is_pending = True
        payment_requests = get_merchant_payment_reqeust(
            account_id=account_id, is_pending=is_pending
        )
        return self.response(
            PaymentRequestResponse(payment_requests, many=True).data
        )


class ListConsumerPaymentRequestAPI(ConsumerAPIView):
    def get(self, request):
        account_id = request.account.id
        pending = self.request_data.get("pending")
        is_pending = False
        if pending == "true":
            is_pending = True
        payment_requests = get_consumer_payment_reqeust(
            account_id=account_id, is_pending=is_pending
        )
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
        data = TransactionHistoryResponse(refund_payment.transaction).data
        SendRefundNotification(
            user_id=refund_payment.payment.order.consumer.user.id, data=data
        ).send()
        RefundReceivedEmail(transaction=refund_payment.transaction).send()
        return self.response(
            RefundHistoryResponse(refund_payment).data, status=201
        )


class RecentStoresAPI(ConsumerAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        orders = get_recent_store_orders(consumer_account=consumer_account)
        return self.response(RecentStoresResponse(orders, many=True).data)
