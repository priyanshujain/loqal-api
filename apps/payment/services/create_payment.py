from decimal import Decimal

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.payment.dbapi import create_transaction
from apps.payment.options import (FACILITATION_FEES_CURRENCY,
                                  FACILITATION_FEES_PERCENTAGE,
                                  TransactionType)
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.provider.options import DEFAULT_CURRENCY
from .check_bank_balance import CheckBankBalance


__all__ = ("CreatePayment",)


class CreatePayment(ServiceBase):
    def __init__(
        self,
        account_id,
        ip_address,
        sender_bank_account,
        receiver_bank_account,
        order,
        total_amount,
        fee_bearer_account,
        amount_towards_order,
        transaction_type=TransactionType.DIRECT_MERCHANT_PAYMENT,
    ):
        self.account_id = account_id
        self.ip_address = ip_address
        self.sender_bank_account = sender_bank_account
        self.receiver_bank_account = receiver_bank_account
        self.order = order
        self.total_amount = total_amount
        self.fee_bearer_account = fee_bearer_account
        self.transaction_type = transaction_type
        self.amount_towards_order = amount_towards_order

    def handle(self):
        transaction = self._factory_transaction()
        balance, error = CheckBankBalance(bank_account=self.sender_bank_account)
        if error:
            transaction.set_balance_check_failed()
        
        dwolla_response = self._send_to_dwolla(transaction=transaction)
        transaction.add_dwolla_id(
            dwolla_id=dwolla_response["dwolla_transfer_id"],
            individual_ach_id=dwolla_response["individual_ach_id"],
            status=dwolla_response["status"],
            amount_towards_order=self.amount_towards_order,
        )
        return transaction


    def _factory_transaction(self):
        payment = self.order.payment
        amount = self.total_amount
        fee_amount = amount * Decimal(FACILITATION_FEES_PERCENTAGE) / 100
        fee_amount = round(fee_amount, 2)

        return create_transaction(
            sender_bank_account_id=self.sender_bank_account.id,
            recipient_bank_account_id=self.receiver_bank_account.id,
            amount=self.total_amount,
            currency=DEFAULT_CURRENCY,
            fee_bearer_account_id=self.fee_bearer_account.id,
            fee_amount=fee_amount,
            fee_currency=FACILITATION_FEES_CURRENCY,
            payment_id=payment.id,
            customer_ip_address=self.ip_address,
            transaction_type=self.transaction_type,
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
        response = self.client.payment.create_new_payment(
            data=psp_request_data
        )
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
            "dwolla_transfer_id": response["data"].get("dwolla_transfer_id"),
            "individual_ach_id": response["data"].get("individual_ach_id"),
        }
