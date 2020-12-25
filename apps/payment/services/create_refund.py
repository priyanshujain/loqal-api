from apps.payment.options import RefundType
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase

from apps.order.dbapi import get_order_by_id
from apps.payment.dbapi import create_refund_payment
from apps.payment.validators import CreateRefundValidator

from .create_payment import CreatePayment
from .validate_bank_balance import ValidateBankBalance

__all__ = ("CreateRefund",)


class CreateRefund(ServiceBase):
    def __init__(self, merchant_account, data, ip_address):
        self.merchant_account = merchant_account
        self.data = data
        self.ip_address = ip_address

    def handle(self):
        payment_data = self._validate_data()
        refund_payment = self._factory_refund_payment(
            payment_data=payment_data
        )
        order = payment_data["order"]

        transaction = CreatePayment(
            account_id=self.merchant_account.id,
            ip_address=self.ip_address,
            sender_bank_account=payment_data["sender_bank_account"],
            sender_bank_balance=payment_data["sender_bank_balance"],
            receiver_bank_account=payment_data["receiver_bank_account"],
            order=order,
            total_amount=refund_payment.amount,
            fee_bearer_account=self.merchant_account.account,
        ).handle()
        refund_payment.add_transaction(transaction=transaction)
        return refund_payment

    def _validate_data(self):
        data = run_validator(CreateRefundValidator, self.data)
        order_id = data["order_id"]
        amount = data["amount"]

        order = get_order_by_id(
            merchant_id=self.merchant_account.id, order_id=order_id
        )
        if not order:
            raise ValidationError(
                {
                    "order_id": ErrorDetail(
                        _("Given order does not exist.")
                    )
                }
            )
        if amount > order.total_net_amount:
            raise ValidationError(
                {
                    "amount": ErrorDetail(
                        _("amount should be less than total order amount.")
                    )
                }
            )
        
        # FIXME: check for the amount to be less than total of all previous refunds

        banking_data = ValidateBankBalance(
            sender_account_id=self.merchant_account.account.id,
            receiver_account_id=order.consumer.account.id,
            total_amount=data["amount"],
        ).validate()

        return {
            "order": order,
            "amount": data["amount"],
            "sender_bank_account": banking_data["sender_bank_account"],
            "receiver_bank_account": banking_data["receiver_bank_account"],
            "sender_bank_balance": banking_data["sender_bank_balance"],
        }

    def _factory_refund_payment(self, payment_data):
        order = payment_data["order"]
        amount = payment_data["amount"]
        refund_type = RefundType.FULL
        if order.total_net_amount > amount:
            refund_type = RefundType.PARTIAL
        return create_refund_payment(
            payment_id=order.payment.id,
            amount=amount,
            refund_type=refund_type
        )