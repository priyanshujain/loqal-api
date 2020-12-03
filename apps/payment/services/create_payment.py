import re
from django.http import request
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.payment.dbapi import create_transaction
from apps.account.dbapi import get_merchant_account
from apps.banking.dbapi import get_bank_account
from apps.payment.validators import CreatePaymentValidator
from apps.payment.options import (
    FACILITATION_FEES_PERCENTAGE,
    FACILITATION_FEES_CURRENCY,
)
from apps.provider.options import DEFAULT_CURRENCY


class CreatePayment(ServiceBase):
    def __init__(self, account_id, data):
        self.data = data
        self.account_id = account_id

    def execute(self):
        payment_data = self._validate_data()
        merchant_account = payment_data["merchant_account"]
        payment_amount = payment_data["payment_amount"]
        payment_currency = payment_data["payment_currency"]

        sender_bank_account = get_bank_account(account_id=self.account_id)
        recipient_bank_account = get_bank_account(
            account_id=merchant_account.account.id
        )

        transaction = self._factory_transaction(
            sender_id=sender_bank_account.id,
            recipient_id=recipient_bank_account.id,
            payment_amount=payment_amount,
            payment_currency=payment_currency,
        )
        dwolla_id = self._send_to_dwolla(transaction=transaction)
        transaction.add_dwolla_id(dwolla_id=dwolla_id)
        return transaction

    def _validate_data(self):
        data = run_validator(CreatePaymentValidator, self.data)
        merchant_id = data["merchant_id"]

        merchant_account = get_merchant_account(account_id=merchant_id)
        if not merchant_account:
            raise ValidationError(
                {"merchant_id": ErrorDetail(_("Given merchant does not exist."))}
            )
        return {
            "merchant_account": merchant_account,
            "payment_amount": data["amount"],
            "payment_currency": DEFAULT_CURRENCY,
        }

    def _factory_transaction(
        self, sender_id, recipient_id, payment_amount, payment_currency
    ):
        fee_value = payment_amount * FACILITATION_FEES_PERCENTAGE / 100
        create_transaction(
            account_id=self.account_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            payment_amount=payment_amount,
            payment_currency=payment_currency,
            fee_value=fee_value,
            fee_currency=FACILITATION_FEES_CURRENCY,
        )

    def _send_to_dwolla(self, transaction):
        api_action = CreateTransferAPIAction(account_id=self.account_id)
        psp_request_data = {
            "sender_bank_account_dwolla_id": transaction.sender.dwolla_id,
            "receiver_bank_account_dwolla_id": transaction.recipient.dwolla_id,
            "receiver_customer_dwolla_id": transaction.recipient.account.dwolla_id,
            "correlation_id": transaction.correlation_id,
            "currency": transaction.payment_currency,
            "amount": transaction.payment_amount,
            "fee_amount": transaction.fee_amount,
            "fee_currency": transaction.fee_currency,
        }
        api_response = api_action.create(data=psp_request_data)
        return api_response["dwolla_transfer_id"]
        
 

from apps.provider.lib.actions import ProviderAPIActionBase
from api.exceptions import ProviderAPIException

class CreateTransferAPIAction(ProviderAPIActionBase):
    def create(self, data):
        response = self.client.payment.create_new_payment(data=data)
        if self.get_errors(response):
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
            "dwolla_transfer_id": response["data"][
                "dwolla_transfer_id"
            ],
        }
