from api.views import UserAPIView
from apps.approval.permissions import IsPaymentApprovalSetPermission
from apps.direct_debit.permissions import CheckDirectDebitExistsPermission
from apps.member.dbapi import get_payment_approvers
from apps.onboarding.permissions import IsAccountApprovedPermission
from apps.payment.dbapi import (get_pending_payment_requests,
                                get_rejected_payment_requests,
                                get_transactions)
from apps.payment.permissions import CreatePaymentPermission
from apps.payment.services import (CreatePayment, ExecutePayment,
                                   PaymentDetails, TransactionConfirmation,
                                   TransactionDetails)

from .responses import (ApproversResponse, PaymentRequestResponse,
                        TransactionResponse)


class CreatePaymentAPI(UserAPIView):
    permission_classes = (
        CreatePaymentPermission,
        IsAccountApprovedPermission,
        CheckDirectDebitExistsPermission,
        IsPaymentApprovalSetPermission,
    )

    def post(self, request):
        account_id = request.account.id
        data = self.request_data
        service_response = self._run_services(account_id=account_id, data=data)
        return self.response(service_response)

    def _run_services(self, account_id, data):
        payment_request_service = CreatePayment(
            account_id=account_id, data=data
        )
        payment_request = payment_request_service.execute()
        if len(data["approver_ids"]) == 0:
            execute_payment_service = ExecutePayment(
                payment_request=payment_request
            )
            transaction = execute_payment_service.execute()
            return TransactionResponse(transaction).data
        else:
            return PaymentRequestResponse(payment_request).data


class ListPendingPaymentRequestAPI(UserAPIView):
    permission_classes = (
        IsAccountApprovedPermission,
        CheckDirectDebitExistsPermission,
    )

    def get(self, request):
        account_id = request.account.id
        payment_requests = get_pending_payment_requests(account_id=account_id)
        return self.paginate(
            request,
            queryset=payment_requests,
            order_by="-created_at",
            response_serializer=PaymentRequestResponse,
        )


class ListRejectedPaymentRequestAPI(UserAPIView):
    permission_classes = (
        IsAccountApprovedPermission,
        CheckDirectDebitExistsPermission,
    )

    def get(self, request):
        account_id = request.account.id
        payment_requests = get_rejected_payment_requests(account_id=account_id)
        return self.paginate(
            request,
            queryset=payment_requests,
            order_by="-created_at",
            response_serializer=PaymentRequestResponse,
        )


class ListTransactionsAPI(UserAPIView):
    permission_classes = (
        CreatePaymentPermission,
        IsAccountApprovedPermission,
        CheckDirectDebitExistsPermission,
        IsPaymentApprovalSetPermission,
    )

    def get(self, request):
        account_id = request.account.id
        transactions = get_transactions(account_id=account_id)
        return self.paginate(
            request,
            queryset=transactions,
            order_by="-created_at",
            response_serializer=TransactionResponse,
        )


class ListPaymentAproversAPI(UserAPIView):
    permission_classes = ()

    def get(self, request):
        account_id = request.account.id
        members = get_payment_approvers(account_id=account_id)
        return self.response(ApproversResponse(members, many=True).data)


class TransactionDetailsAPI(UserAPIView):
    permission_classes = (
        CreatePaymentPermission,
        IsAccountApprovedPermission,
        CheckDirectDebitExistsPermission,
        IsPaymentApprovalSetPermission,
    )

    def get(self, request, transaction_id):
        account_id = request.account.id
        transaction = self._run_services(
            account_id=account_id, transaction_id=transaction_id
        )
        if not transaction:
            return self.response(status=404)
        return self.response(TransactionResponse(transaction).data)

    def _run_services(self, account_id, transaction_id):
        service = TransactionDetails(
            account_id=account_id, transaction_id=transaction_id
        )
        return service.execute()


class PaymentRequestDetailAPI(UserAPIView):
    permission_classes = (
        CreatePaymentPermission,
        IsAccountApprovedPermission,
        CheckDirectDebitExistsPermission,
        IsPaymentApprovalSetPermission,
    )

    def get(self, request, payment_request_id):
        account_id = request.account.id
        payment_request = self._run_services(
            account_id=account_id, payment_request_id=payment_request_id
        )
        if not payment_request:
            return self.response(status=404)
        return self.response(PaymentRequestResponse(payment_request).data)

    def _run_services(self, account_id, payment_request_id):
        service = PaymentDetails(
            account_id=account_id, payment_request_id=payment_request_id
        )
        return service.execute()


class TransactionConfirmationFileAPI(UserAPIView):
    permission_classes = (
        CreatePaymentPermission,
        IsAccountApprovedPermission,
        CheckDirectDebitExistsPermission,
        IsPaymentApprovalSetPermission,
    )

    def get(self, request, transaction_id):
        account_id = request.account.id
        file_url = self._run_services(
            account_id=account_id, transaction_id=transaction_id
        )
        return self.response({"file_url": file_url})

    def _run_services(self, account_id, transaction_id):
        # FIX: Apply a check for getting file for second time
        #  from DB once downloaded from provider
        service = TransactionConfirmation(
            account_id=account_id, transaction_id=transaction_id
        )
        return service.execute()
