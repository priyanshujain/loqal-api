from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.payment.dbapi import create_payment, create_transaction
from apps.payment.options import (
    FACILITATION_FEES_CURRENCY,
    FACILITATION_FEES_PERCENTAGE,
)
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.provider.options import DEFAULT_CURRENCY


__all__ = ("CreatePayment",)


class CreatePayment(ServiceBase):
    def __init__(
        self,
        account_id,
        ip_address,
        sender_bank_account,
        sender_bank_balance,
        receiver_bank_account,
        order,
        total_amount,
        fee_bearer_account,
    ):
        self.account_id = account_id
        self.ip_address = ip_address
        self.sender_bank_account = sender_bank_account
        self.sender_bank_balance = sender_bank_balance
        self.receiver_bank_account = receiver_bank_account
        self.order = order
        self.total_amount = total_amount
        self.fee_bearer_account = fee_bearer_account

    def handle(self):
        assert self._validate_data()
        transaction = self._factory_transaction()
        dwolla_response = self._send_to_dwolla(transaction=transaction)
        transaction.add_dwolla_id(
            dwolla_id=dwolla_response["dwolla_transfer_id"],
            status=dwolla_response["status"],
        )
        return transaction

    def _validate_data(self):
        if not self.sender_bank_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Sender bank account is not valid."))}
            )
        if not self.sender_bank_balance:
            raise ValidationError(
                {"detail": ErrorDetail(_("Sender bank balance is not valid."))}
            )
        if not self.receiver_bank_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Receiver bank account is not valid."))}
            )
        if not self.order:
            raise ValidationError({"detail": ErrorDetail(_("Order is not valid."))})
        if not self.total_amount:
            raise ValidationError({"detail": ErrorDetail(_("Amount is not valid."))})
        if not self.fee_bearer_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Fee bearer account is not valid."))}
            )
        return True

    def _factory_transaction(self):
        payment = self.order.payment
        amount = self.total_amount
        fee_amount = amount * FACILITATION_FEES_PERCENTAGE / 100
        fee_amount = round(fee_amount, 2)

        return create_transaction(
            sender_bank_account_id=self.sender_bank_account.id,
            recipient_bank_account_id=self.receiver_bank_account.id,
            sender_balance_at_checkout=self.sender_bank_balance,
            amount=self.total_amount,
            currency=DEFAULT_CURRENCY,
            fee_bearer_account_id=self.fee_bearer_account.id,
            fee_amount=fee_amount,
            fee_currency=FACILITATION_FEES_CURRENCY,
            payment_id=payment.id,
            customer_ip_address=self.ip_address,
        )

    def _send_to_dwolla(self, transaction):
        api_action = CreateTransferAPIAction(account_id=self.account_id)
        api_response = api_action.create(transaction=transaction)
        return api_response


class CreateTransferAPIAction(ProviderAPIActionBase):
    def create(self, transaction):
        psp_request_data = {
            "sender_bank_account_dwolla_id": transaction.sender_bank_account.dwolla_id,
            "receiver_bank_account_dwolla_id": transaction.recipient_bank_account.dwolla_id,
            "fee_bearer_dwolla_id": transaction.fee_bearer_account.dwolla_id,
            "correlation_id": transaction.correlation_id,
            "currency": transaction.currency,
            "amount": float(transaction.amount),
            "fee_amount": float(transaction.fee_amount),
            "fee_currency": transaction.fee_currency,
        }
        response = self.client.payment.create_new_payment(data=psp_request_data)
        if self.get_errors(response):
            transaction.set_internal_error()
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return {
            "status": response["data"].get("status"),
            "dwolla_transfer_id": response["data"]["dwolla_transfer_id"],
        }
