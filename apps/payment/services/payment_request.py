from decimal import Decimal

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import (
    get_consumer_account_by_phone_number,
    get_consumer_account_by_username,
)
from apps.banking.dbapi import get_bank_account
from apps.merchant.services import InviteConsumerBySMS
from apps.order.options import OrderType
from apps.order.services import CreateOrder
from apps.payment.dbapi import (
    create_payment,
    create_payment_request,
    create_transaction,
    get_merchant_receive_limit,
    get_payment_reqeust_by_uid,
)
from apps.payment.dbapi.events import (
    capture_payment_event,
    failed_payment_event,
    initiate_payment_event,
    failure_partial_return_event,
)
from apps.payment.options import (
    PaymentProcess,
    PaymentRequestStatus,
    TransactionTransferTypes,
    TransactionType,
    TransactionSourceTypes,
)
from apps.payment.validators import (
    ApprovePaymentRequestValidator,
    CreatePaymentRequestValidator,
    RejectPaymentRequestValidator,
)
from apps.provider.options import DEFAULT_CURRENCY

from .create_payment import CreatePayment
from .validate_bank_account import ValidateBankAccount
from apps.reward.options import RewardValueType
from apps.reward.services import FullReturnRewards


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
            consumer_account = get_consumer_account_by_username(username=loqal_id)

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
            raise ValidationError({"detail": ErrorDetail(_("Invalid account."))})

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

        order, reward_usage = CreateOrder(
            consumer_id=consumer_account.id,
            merchant_id=merchant_account.id,
            amount=payment_request.amount,
            order_type=OrderType.ONLINE,
        ).handle()

        applied_cashback_amount = Decimal(0.0)
        if reward_usage:
            if reward_usage.reward_value_type == RewardValueType.FIXED_AMOUNT:
                applied_cashback_amount = reward_usage.total_amount

        total_payable_amount = (
            order.total_net_amount - applied_cashback_amount + data["tip_amount"]
        )
        payment = create_payment(
            order_id=order.id, payment_process=PaymentProcess.PAYMENT_REQUEST
        )
        initiate_payment_event(payment_id=payment.id)
        payment_request.add_payment(payment=payment, tip_amount=data["tip_amount"])

        if total_payable_amount > Decimal(0.0):
            try:
                transaction = CreatePayment(
                    account_id=self.account_id,
                    ip_address=self.ip_address,
                    sender_bank_account=banking_data["sender_bank_account"],
                    receiver_bank_account=banking_data["receiver_bank_account"],
                    order=payment_request.payment.order,
                    total_amount=total_payable_amount,
                    amount_towards_order=(total_payable_amount - data["tip_amount"]),
                    fee_bearer_account=merchant_account.account,
                    transaction_type=TransactionType.PAYMENT_REQUEST,
                    payment_request_id=payment_request.id,
                ).handle()
                capture_payment_event(
                    payment_id=transaction.payment.id,
                    transaction_tracking_id=transaction.transaction_tracking_id,
                )
                payment_request.set_accepted()
            except Exception as error:
                transaction_tracking_id = None
                payment_request.set_failed()
                try:
                    transaction = error.transaction
                    transaction_tracking_id = transaction.transaction_tracking_id
                except AttributeError:
                    pass
                failed_payment_event(
                    payment_id=payment_request.payment.id,
                    transaction_tracking_id=transaction_tracking_id,
                    amount=total_payable_amount,
                    transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
                )
                if reward_usage:
                    FullReturnRewards(reward_usage=reward_usage).handle()
                    if applied_cashback_amount:
                        failure_partial_return_event(
                            payment_id=payment_request.payment.id,
                            transaction_tracking_id=None,
                            amount=applied_cashback_amount,
                            transfer_type=TransactionTransferTypes.CASHBACK,
                        )
                raise error

            if applied_cashback_amount > Decimal(0.0):
                transaction = create_transaction(
                    transaction_type=TransactionType.DIRECT_MERCHANT_PAYMENT,
                    payment_id=payment_request.payment.id,
                    amount=applied_cashback_amount,
                    fee_bearer_account_id=payment_request.account.id,
                    customer_ip_address=self.ip_address,
                    sender_source_type=TransactionSourceTypes.REWARD_CASHBACK,
                    recipient_source_type=TransactionSourceTypes.NA,
                    payment_request_id=payment_request.id,
                    reward_usage_id=reward_usage.id,
                    is_success=True,
                )
                payment_request.payment.capture_payment(
                    amount=applied_cashback_amount,
                    amount_towards_order=applied_cashback_amount,
                )
                capture_payment_event(
                    payment_id=payment_request.payment.id,
                    transaction_tracking_id=transaction.transaction_tracking_id,
                    amount=applied_cashback_amount,
                    transfer_type=TransactionTransferTypes.CASHBACK,
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
                {"detail": ErrorDetail(_("Given payment request is no longer valid."))}
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
                {"detail": ErrorDetail(_("Given payment request is no longer valid."))}
            )
        return payment_request
