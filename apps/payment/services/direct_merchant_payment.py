from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import get_merchant_account_by_uid
from apps.account.options import DwollaCustomerStatus
from apps.order.dbapi import create_payment_request_order
from apps.payment.dbapi import (create_direct_merchant_payment, create_payment,
                                get_payment_qrcode)
from apps.payment.dbapi.events import (capture_payment_event,
                                       initiate_payment_event)
from apps.payment.options import PaymentProcess, TransactionType
from apps.payment.validators import CreateMerchantPaymentValidator
from apps.provider.options import DEFAULT_CURRENCY

from .create_payment import CreatePayment
from .validate_bank_account import ValidateBankAccount

__all__ = ("DirectMerchantPayment",)


class DirectMerchantPayment(ServiceBase):
    def __init__(self, consumer_account, data, ip_address):
        self.consumer_account = consumer_account
        self.data = data
        self.ip_address = ip_address

    def handle(self):
        payment_data = self._validate_data()
        merhcant_payment = self._factory_merchant_payment(
            payment_data=payment_data
        )
        total_amount = payment_data["amount"] + payment_data["tip_amount"]
        merhcant_account = payment_data["merchant_account"]

        transaction = CreatePayment(
            account_id=self.consumer_account.id,
            ip_address=self.ip_address,
            sender_bank_account=payment_data["sender_bank_account"],
            receiver_bank_account=payment_data["receiver_bank_account"],
            order=merhcant_payment.payment.order,
            total_amount=total_amount,
            amount_towards_order=payment_data["amount"],
            fee_bearer_account=merhcant_account.account,
            transaction_type=TransactionType.DIRECT_MERCHANT_PAYMENT,
        ).handle()
        capture_payment_event(
            payment_id=transaction.payment.id,
            transaction_tracking_id=transaction.transaction_tracking_id,
        )
        merhcant_payment.add_transaction(transaction=transaction)
        return merhcant_payment

    def _validate_data(self):
        data = run_validator(CreateMerchantPaymentValidator, self.data)
        merchant_id = data["merchant_id"]

        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_id
        )
        if not merchant_account:
            raise ValidationError(
                {
                    "merchant_id": ErrorDetail(
                        _("Given merchant does not exist.")
                    )
                }
            )

        if (
            merchant_account.account.dwolla_verification_status
            != DwollaCustomerStatus.VERIFIED
        ):
            raise ValidationError(
                {
                    "merchant_id": ErrorDetail(
                        _("Merchant account is not active yet.")
                    )
                }
            )

        qrcode_id = data.get("qrcode_id")
        if qrcode_id:
            payment_qrcode = get_payment_qrcode(qrcode_id=qrcode_id)
            if not payment_qrcode:
                raise ValidationError(
                    {"qrcode_id": [ErrorDetail(_("Invalid QR code."))]}
                )
            if payment_qrcode.merchant != merchant_account:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            "QR Code does not belong to provided merchant."
                        )
                    }
                )
            payment_qrcode_id = payment_qrcode.id
        else:
            payment_qrcode_id = None

        banking_data = ValidateBankAccount(
            sender_account_id=self.consumer_account.account.id,
            receiver_account_id=merchant_account.account.id,
        ).validate()

        return {
            "merchant_account": merchant_account,
            "amount": data["amount"],
            "tip_amount": data["tip_amount"],
            "currency": DEFAULT_CURRENCY,
            "payment_qrcode_id": payment_qrcode_id,
            "sender_bank_account": banking_data["sender_bank_account"],
            "receiver_bank_account": banking_data["receiver_bank_account"],
        }

    def _factory_merchant_payment(self, payment_data):
        merchant_id = payment_data["merchant_account"].id
        consumer_id = self.consumer_account.id
        amount = payment_data["amount"]
        tip_amount = payment_data["tip_amount"]
        payment_qrcode_id = payment_data["payment_qrcode_id"]
        order = create_payment_request_order(
            merchant_id=merchant_id,
            consumer_id=consumer_id,
            amount=amount,
        )
        payment_process = PaymentProcess.DIRECT_APP
        if payment_qrcode_id:
            payment_process = PaymentProcess.QRCODE
        payment = create_payment(
            order_id=order.id, payment_process=payment_process
        )
        initiate_payment_event(payment_id=payment.id)
        return create_direct_merchant_payment(
            payment_id=payment.id,
            tip_amount=tip_amount,
            payment_qrcode_id=payment_qrcode_id,
        )
