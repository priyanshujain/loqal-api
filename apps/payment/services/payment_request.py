from decimal import Decimal

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import (get_consumer_account_by_phone_number,
                                get_consumer_account_by_username)
from apps.banking.dbapi import get_bank_account
from apps.merchant.services import InviteConsumerBySMS
from apps.order.dbapi import create_payment_request_order
from apps.payment.dbapi import (create_payment, create_payment_request,
                                get_merchant_receive_limit,
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

        if not consumer_account:
            if is_phone_number_based:
                is_success = False
                try:
                    is_success = InviteConsumerBySMS(
                        merchant=merchant_account,
                        phone_number=phone_number,
                        request_payment=True,
                    ).handle()
                except Exception:
                    pass
                if is_success:
                    raise ValidationError(
                        {
                            "detail": [
                                ErrorDetail(
                                    "Given phone number is not registered "
                                    "with Loqal. We have sent an SMS invite "
                                    "to this number to download the Loqal App."
                                )
                            ]
                        }
                    )
                raise ValidationError(
                    {
                        "detail": [
                            ErrorDetail(
                                "Given phone number/ Loqal ID is not vaild. Please check and try again."
                            )
                        ]
                    }
                )

        amount = data["amount"]
        merchant_receive_limit = get_merchant_receive_limit(
            merchant_id=merchant_account.id
        )
        if merchant_receive_limit:
            if amount > merchant_receive_limit.transaction_limit:
                raise ValidationError(
                    {
                        "detail": [
                            ErrorDetail(
                                "Payment request amount limit exceeded. "
                                "Your store is set to receive upto "
                                f"${merchant_receive_limit.transaction_limit} per transaction."
                                " If you want to increase your limit please email us at hello@loqal.us."
                            )
                        ]
                    }
                )
        data["account_to_id"] = consumer_account.account.id
        data["consumer_id"] = consumer_account.id
        data["merchant_id"] = merchant_account.id
        return data

    def _factory_payment_request(self, data):
        order = create_payment_request_order(
            merchant_id=data["merchant_id"],
            consumer_id=data["consumer_id"],
            amount=data["amount"],
        )
        payment = create_payment(
            order_id=order.id, payment_process=PaymentProcess.PAYMENT_REQUEST
        )
        initiate_payment_event(payment_id=payment.id)
        return create_payment_request(
            account_from_id=self.account_id,
            account_to_id=data["account_to_id"],
            payment_id=payment.id,
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

        total_amount = payment_request.amount + data["tip_amount"]
        banking_data = ValidateBankAccount(
            sender_account_id=self.account_id,
            receiver_account_id=merchant_account.account.id,
        ).validate()

        try:
            transaction = CreatePayment(
                account_id=self.account_id,
                ip_address=self.ip_address,
                sender_bank_account=banking_data["sender_bank_account"],
                receiver_bank_account=banking_data["receiver_bank_account"],
                order=payment_request.payment.order,
                total_amount=total_amount,
                amount_towards_order=payment_request.amount,
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
