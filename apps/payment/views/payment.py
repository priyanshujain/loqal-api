from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView, MerchantAPIView, PosStaffAPIView
from apps.merchant.services.member import account_member
from apps.payment.dbapi import (create_empty_transactions,
                                get_consumer_payment_reqeust,
                                get_consumer_transaction,
                                get_consumer_transactions,
                                get_merchant_payment_reqeust,
                                get_recent_store_orders, register)
from apps.payment.notifications import (SendApproveRequestNotification,
                                        SendNewPaymentNotification,
                                        SendNewPaymentRequestNotification,
                                        SendRefundNotification,
                                        SendRejectRequestNotification)
from apps.payment.notifications.email import (RefundReceivedEmail,
                                              SendPaymentInitiatedEmail)
from apps.payment.options import TransactionSourceTypes
from apps.payment.responses import (ConsumerPaymentRequestResponse,
                                    CreateRefundResponse,
                                    CreateTransactionResponse,
                                    MerchantTransactionHistoryResponse,
                                    PaymentRequestResponse,
                                    RecentStoresResponse,
                                    RefundHistoryResponse,
                                    RefundTransactionsResponse,
                                    TransactionDetailsResponse,
                                    TransactionHistoryResponse)
from apps.payment.services import (ApprovePaymentRequest, CreatePaymentRequest,
                                   CreateRefund, DirectMerchantPayment,
                                   RejectPaymentRequest)
from apps.payment.tasks import create_staff_payment_notification
from apps.reward.services import AllocateRewards


class CreatePaymentAPI(ConsumerAPIView):
    def post(self, request):
        consumer_account = request.consumer_account
        merchant_payment = DirectMerchantPayment(
            consumer_account=consumer_account,
            data=self.request_data,
            ip_address=request.ip,
        ).handle()
        transactions = create_empty_transactions()
        try:
            transactions = merchant_payment.transactions.all()
        except Exception:
            pass
        payment_response = {}
        payment_response["transactions"] = CreateTransactionResponse(
            transactions, many=True
        ).data
        payment_response["tip_amount"] = merchant_payment.tip_amount
        payment_notification_data = {}
        payment_notification_data[
            "transactions"
        ] = MerchantTransactionHistoryResponse(
            transactions,
            many=True,
        ).data
        payment_notification_data["tip_amount"] = str(
            merchant_payment.tip_amount
        )
        try:
            reward = AllocateRewards(
                payment=merchant_payment.payment, ip_address=request.ip
            ).handle()
            if reward:
                payment_response["reward"] = reward
        except Exception:
            pass
        create_staff_payment_notification(
            payment_id=merchant_payment.payment.id
        )
        SendNewPaymentNotification(
            merchant_id=merchant_payment.payment.order.merchant.id,
            data=payment_notification_data,
        ).send()
        banking_transactions = transactions.filter(
            sender_source_type=TransactionSourceTypes.BANK_ACCOUNT
        )
        if banking_transactions.exists():
            SendPaymentInitiatedEmail(
                transaction=banking_transactions.first()
            ).send()
        return self.response(payment_response, status=201)


class PaymentHistoryAPI(ConsumerAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        transactions = get_consumer_transactions(
            consumer_account=consumer_account
        )
        return self.paginate(
            request,
            queryset=transactions,
            order_by="-created_at",
            response_serializer=TransactionHistoryResponse,
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
        merchant_account_member = request.merchant_account_member
        payment_request = CreatePaymentRequest(
            account_id=account_id,
            account_member_id=merchant_account_member.id,
            register_id=None,
            data=self.request_data,
        ).handle()
        SendNewPaymentRequestNotification(
            user_id=payment_request.account_to.consumer.user.id,
            data=ConsumerPaymentRequestResponse(payment_request).data,
        ).send()
        return self.response(
            PaymentRequestResponse(payment_request).data, status=201
        )


class CreatePosPaymentRequestAPI(PosStaffAPIView):
    def post(self, request):
        account_id = request.account.id
        pos_staff = request.pos_staff
        payment_request = CreatePaymentRequest(
            account_id=account_id,
            account_member_id=None,
            register_id=pos_staff.register.id,
            data=self.request_data,
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
        transactions = create_empty_transactions()
        try:
            transactions = payment_request.transactions.all()
        except Exception:
            pass
        payment_response = {}
        payment_response["transactions"] = CreateTransactionResponse(
            transactions, many=True
        ).data
        payment_response["tip_amount"] = payment_request.tip_amount
        payment_notification_data = {}
        payment_notification_data[
            "transactions"
        ] = MerchantTransactionHistoryResponse(
            transactions,
            many=True,
        ).data
        payment_notification_data["tip_amount"] = str(
            payment_request.tip_amount
        )
        create_staff_payment_notification(
            payment_id=payment_request.payment.id
        )
        SendNewPaymentNotification(
            merchant_id=payment_request.payment.order.merchant.id,
            data=payment_notification_data,
        ).send()
        try:
            reward = AllocateRewards(
                payment=payment_request.payment, ip_address=request.ip
            ).handle()
            if reward:
                payment_response["reward"] = reward
        except Exception:
            pass
        SendApproveRequestNotification(
            merchant_id=payment_request.payment.order.merchant.id,
            data={
                "payment_request_id": str(payment_request.u_id),
                "payment_id": payment_request.payment.payment_tracking_id,
            },
        ).send()
        banking_transactions = transactions.filter(
            sender_source_type=TransactionSourceTypes.BANK_ACCOUNT
        )
        if banking_transactions.exists():
            SendPaymentInitiatedEmail(
                transaction=banking_transactions.first()
            ).send()
        return self.response(payment_response)


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
        return self.paginate(
            request,
            queryset=payment_requests,
            order_by="-created_at",
            response_serializer=PaymentRequestResponse,
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
        merchant_account_member = request.merchant_account_member
        refund_payment = CreateRefund(
            merchant_account=merchant_account,
            account_member_id=merchant_account_member.id,
            data=self.request_data,
            ip_address=request.ip,
        ).handle()
        transactions = create_empty_transactions()
        try:
            transactions = refund_payment.transactions.all()
        except Exception:
            pass
        data = CreateTransactionResponse(transactions, many=True).data
        SendRefundNotification(
            user_id=refund_payment.payment.order.consumer.user.id, data=data
        ).send()
        banking_transactions = transactions.filter(
            recipient_source_type=TransactionSourceTypes.BANK_ACCOUNT
        )
        if banking_transactions.exists():
            RefundReceivedEmail(
                transaction=banking_transactions.first()
            ).send()
        refund_response = RefundHistoryResponse(refund_payment).data
        refund_response["transactions"] = RefundTransactionsResponse(
            transactions, many=True
        ).data
        return self.response(refund_response, status=201)


class RecentStoresAPI(ConsumerAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        orders = get_recent_store_orders(consumer_account=consumer_account)
        return self.response(RecentStoresResponse(orders, many=True).data)
