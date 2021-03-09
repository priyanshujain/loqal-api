from decimal import Decimal

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import (get_consumer_account_by_phone_number,
                                get_consumer_account_by_username)
from apps.banking.dbapi import get_bank_account
from apps.order.dbapi import create_payment_request_order
from apps.order.options import OrderType
from apps.order.services import CreateOrder
from apps.payment.dbapi import (create_payment, create_payment_request,
                                create_zero_transaction,
                                get_payment_reqeust_by_uid)
from apps.payment.dbapi.events import (cancelled_payment_event,
                                       capture_payment_event,
                                       failed_payment_event,
                                       initiate_payment_event)
from apps.payment.options import (PaymentProcess, PaymentRequestStatus,
                                  TransactionType)
from apps.payment.validators import (ApprovePaymentRequestValidator,
                                     CreatePaymentRequestValidator,
                                     RejectPaymentRequestValidator)
from apps.provider.options import DEFAULT_CURRENCY

from .create_payment import CreatePayment
from .validate_bank_account import ValidateBankAccount

__all__ = (
    "CreatePaymentRequest",
    "ApprovePaymentRequest",
    "RejectPaymentRequest",
)


class CreatePaymentRequest(ServiceBase):
    def __init__(self, account_id, data):
        self.data = data
        self.account_id = account_id

    def handle(self):
        payment_data = self._validate_data()
        payment_request = self._factory_payment_request(data=payment_data)
        return payment_request

    def _validate_data(self):
        data = run_validator(CreatePaymentRequestValidator, self.data)
        is_phone_number_based = data.get("is_phone_number_based")
        loqal_id = data.get("requested_to_loqal_id")
        phone_number = data.get("requested_to_phone_number")

        if is_phone_number_based:
            consumer_account = get_consumer_account_by_phone_number(
                phone_number=phone_number
            )
        else:
            consumer_account = get_consumer_account_by_username(
                username=loqal_id
            )

        bank_account = get_bank_account(account_id=self.account_id)
        if not bank_account:
            raise ValidationError(
                {
                    "detail": [
                        ErrorDetail(
                            "Please add receiving bank account before creating payment request."
                        )
                    ]
                }
            )
        try:
            merchant_account = bank_account.account.merchant
        except AttributeError:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid account."))}
            )
        data["account_to_id"] = consumer_account.account.id
        data["consumer_id"] = consumer_account.id
        data["merchant_id"] = merchant_account.id
        return data

    def _factory_payment_request(self, data):
        return create_payment_request(
            account_from_id=self.account_id,
            account_to_id=data["account_to_id"],
            amount=data["amount"],
            currency=DEFAULT_CURRENCY,
        )


class ApprovePaymentRequest(ServiceBase):
    def __init__(
        self,
        account_id,
        data,
        ip_address,
    ):
        self.data = data
        self.account_id = account_id
        self.ip_address = ip_address

    def handle(self):
        data = self._validate_data()
        payment_request = data["payment_request"]

        try:
            merchant_account = payment_request.account_from.merchant
        except AttributeError:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid payment request."))}
            )

        try:
            consumer_account = payment_request.account_to.consumer
        except AttributeError:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid payment request."))}
            )

        banking_data = ValidateBankAccount(
            sender_account_id=self.account_id,
            receiver_account_id=merchant_account.account.id,
        ).validate()

        order = CreateOrder(
            consumer_id=consumer_account.id,
            merchant_id=merchant_account.id,
            amount=payment_request.amount,
            order_type=OrderType.ONLINE,
        ).handle()
        total_amount = order.total_net_amount + data["tip_amount"]
        payment = create_payment(
            order_id=order.id, payment_process=PaymentProcess.PAYMENT_REQUEST
        )
        payment_request.add_payment(payment)
        if total_amount == Decimal(0.0):
            payment_request.payment.process_zero_payment()
            capture_payment_event(
                payment_id=payment_request.payment.id,
                transaction_tracking_id=None,
            )
            transaction = create_zero_transaction(
                customer_ip_address=self.ip_address,
                sender_bank_account=banking_data["sender_bank_account"],
                recipient_bank_account=banking_data["receiver_bank_account"],
                transaction_type=TransactionType.DIRECT_MERCHANT_PAYMENT,
                payment_id=payment_request.payment.id,
            )
            payment_request.add_transaction(
                transaction=transaction, tip_amount=data["tip_amount"]
            )
            return payment_request

        try:
            transaction = CreatePayment(
                account_id=self.account_id,
                ip_address=self.ip_address,
                sender_bank_account=banking_data["sender_bank_account"],
                receiver_bank_account=banking_data["receiver_bank_account"],
                order=payment_request.payment.order,
                total_amount=total_amount,
                amount_towards_order=order.total_net_amount,
                fee_bearer_account=merchant_account.account,
                transaction_type=TransactionType.PAYMENT_REQUEST,
            ).handle()
        except Exception as error:
            is_save = False
            transaction_tracking_id = None
            payment_request.set_failed(save=False)
            try:
                transaction = error.transaction
                payment_request.add_transaction(
                    transaction=transaction, tip_amount=data["tip_amount"]
                )
                transaction_tracking_id = transaction.transaction_tracking_id
                is_save = True
            except AttributeError:
                pass
            if not is_save:
                payment_request.save()
            failed_payment_event(
                payment_id=payment_request.payment.id,
                transaction_tracking_id=transaction_tracking_id,
            )
            raise error
        capture_payment_event(
            payment_id=transaction.payment.id,
            transaction_tracking_id=transaction.transaction_tracking_id,
        )
        payment_request.add_transaction(
            transaction=transaction, tip_amount=data["tip_amount"]
        )
        return payment_request

    def _validate_data(self):
        data = run_validator(ApprovePaymentRequestValidator, data=self.data)
        payment_request_id = data["payment_request_id"]

        payment_request = get_payment_reqeust_by_uid(
            payment_request_id=payment_request_id,
            account_to_id=self.account_id,
        )
        if not payment_request:
            raise ValidationError(
                {
                    "payment_request_id": [
                        ErrorDetail(_("Payment request is not valid."))
                    ]
                }
            )
        if payment_request.status != PaymentRequestStatus.REQUEST_SENT:
            raise ValidationError(
                {"detail": [ErrorDetail(_("Payment request is expired."))]}
            )
        receiver_account = payment_request.account_to
        if not receiver_account.is_active:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Given payment request is no longer valid.")
                    )
                }
            )
        data["payment_request"] = payment_request
        return data


class RejectPaymentRequest(ServiceBase):
    def __init__(
        self,
        account_id,
        data,
    ):
        self.data = data
        self.account_id = account_id

    def handle(self):
        payment_request = self._validate_data()
        payment_request.reject()
        cancelled_payment_event(payment_id=payment_request.payment.id)
        return payment_request

    def _validate_data(self):
        data = run_validator(RejectPaymentRequestValidator, data=self.data)
        payment_request_id = data["payment_request_id"]

        payment_request = get_payment_reqeust_by_uid(
            payment_request_id=payment_request_id,
            account_to_id=self.account_id,
        )
        if not payment_request:
            raise ValidationError(
                {
                    "payment_request_id": [
                        ErrorDetail(_("Payment request is not valid."))
                    ]
                }
            )
        if payment_request.status != PaymentRequestStatus.REQUEST_SENT:
            raise ValidationError(
                {"detail": ErrorDetail(_("Payment request is expired."))}
            )
        receiver_account = payment_request.account_to
        if not receiver_account.is_active:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Given payment request is no longer valid.")
                    )
                }
            )
        return payment_request
