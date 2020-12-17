from django.conf import settings
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import get_merchant_account_by_uid
from apps.account.options import AccountStatus
from apps.banking.dbapi import get_bank_account
from apps.payment.dbapi import create_transaction, get_payment_qrcode
from apps.payment.options import (FACILITATION_FEES_CURRENCY,
                                  FACILITATION_FEES_PERCENTAGE)
from apps.payment.validators import CreatePaymentValidator
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.provider.options import DEFAULT_CURRENCY
from integrations.utils.options import RequestStatusTypes
from plugins.plaid import PlaidPlugin

__all__ = ("CreatePayment",)


class CreatePayment(ServiceBase):
    def __init__(self, account_id, data):
        self.data = data
        self.account_id = account_id

    def handle(self):
        payment_data = self._validate_data()
        merchant_account = payment_data["merchant_account"]
        payment_amount = payment_data["payment_amount"]
        tip_amount = payment_data["tip_amount"]
        payment_currency = payment_data["payment_currency"]
        payment_qrcode_id = payment_data["payment_qrcode_id"]

        sender_bank_account = get_bank_account(account_id=self.account_id)

        if not sender_bank_account:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        "Please add the bank account before making payment."
                    )
                }
            )

        recipient_bank_account = get_bank_account(
            account_id=merchant_account.account.id
        )
        if not recipient_bank_account:
            raise ValidationError(
                {"detail": ErrorDetail("Merchant account is not active yet.")}
            )

        balance = self._check_balance(bank_account=sender_bank_account)
        min_required_balance = (
            payment_amount
            + tip_amount
            + settings.MIN_BANK_ACCOUNT_BALANCE_REQUIRED
        )
        if balance < min_required_balance:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        "You need minimum $100 excess of given amount to make a payment."
                    )
                }
            )

        transaction = self._factory_transaction(
            sender_id=sender_bank_account.id,
            recipient_id=recipient_bank_account.id,
            payment_amount=payment_amount,
            tip_amount=tip_amount,
            payment_currency=payment_currency,
            payment_qrcode_id=payment_qrcode_id,
        )
        dwolla_id = self._send_to_dwolla(transaction=transaction)
        transaction.add_dwolla_id(dwolla_id=dwolla_id)
        return transaction

    def _validate_data(self):
        data = run_validator(CreatePaymentValidator, self.data)
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

        if merchant_account.account_status != AccountStatus.VERIFIED:
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

        return {
            "merchant_account": merchant_account,
            "payment_amount": data["payment_amount"],
            "tip_amount": data["tip_amount"],
            "payment_currency": DEFAULT_CURRENCY,
            "payment_qrcode_id": payment_qrcode_id,
        }

    def _check_balance(self, bank_account):
        plaid = PlaidPlugin()
        balance = plaid.get_balance(
            access_token=bank_account.plaid_access_token,
            account_id=bank_account.plaid_account_id,
        )
        if not balance:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Balance check failed, please try again.")
                    )
                }
            )
        return balance

    def _factory_transaction(
        self,
        sender_id,
        recipient_id,
        payment_amount,
        tip_amount,
        payment_currency,
        payment_qrcode_id,
    ):
        fee_amount = payment_amount * FACILITATION_FEES_PERCENTAGE / 100
        fee_amount = round(fee_amount, 2)

        return create_transaction(
            account_id=self.account_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            payment_amount=payment_amount,
            tip_amount=tip_amount,
            payment_currency=payment_currency,
            fee_amount=fee_amount,
            fee_currency=FACILITATION_FEES_CURRENCY,
            payment_qrcode_id=payment_qrcode_id,
        )

    def _send_to_dwolla(self, transaction):
        api_action = CreateTransferAPIAction(account_id=self.account_id)
        total_amount = transaction.payment_amount + transaction.tip_amount

        psp_request_data = {
            "sender_bank_account_dwolla_id": transaction.sender.dwolla_id,
            "receiver_bank_account_dwolla_id": transaction.recipient.dwolla_id,
            "receiver_customer_dwolla_id": transaction.recipient.account.dwolla_id,
            "correlation_id": transaction.correlation_id,
            "currency": transaction.payment_currency,
            "amount": total_amount,
            "fee_amount": transaction.fee_amount,
            "fee_currency": transaction.fee_currency,
        }
        api_response = api_action.create(data=psp_request_data)
        if api_response["status"] == RequestStatusTypes.ERROR:
            transaction.delete()
        return api_response["dwolla_transfer_id"]


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
            "dwolla_transfer_id": response["data"]["dwolla_transfer_id"],
        }
