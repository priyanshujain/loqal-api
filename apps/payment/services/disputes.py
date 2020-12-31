from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.payment.dbapi import (
    create_dispute_transaction,
    get_consumer_transaction,
    get_dispute_transaction,
)
from apps.payment.validators import CreateDisputeValidator
from apps.payment.options import TransactionType
from apps.payment.dbapi.events import dispute_payment_event


__all__ = ("CreateDispute",)


class CreateDispute(ServiceBase):
    def __init__(self, consumer_account, data):
        self.consumer_account = consumer_account
        self.data = data

    def handle(self):
        dispute_data = self._validate_data()
        transaction = dispute_data["transaction"]
        dispute = self._factory_dispute(
            transaction_id=transaction.id,
            reason_message=dispute_data["reason_message"],
            reason_type=dispute_data["reason_type"],
        )
        transaction.enable_disputed()
        return dispute

    def _validate_data(self):
        data = run_validator(CreateDisputeValidator, self.data)
        transaction_tracking_id = data["transaction_tracking_id"]
        transaction = get_consumer_transaction(
            consumer_account=self.consumer_account,
            transaction_tracking_id=transaction_tracking_id,
        )

        if not transaction:
            raise ValidationError(
                {
                    "transaction_tracking_id": ErrorDetail(
                        _("Given transaction does not exist.")
                    )
                }
            )

        dispute = get_dispute_transaction(transaction_id=transaction.id)
        if dispute:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Dispute already exists for this transaction.")
                    )
                }
            )

        if transaction.transaction_type in [
            TransactionType.PAYMENT_REQUEST,
            TransactionType.DIRECT_MERCHANT_PAYMENT,
        ]:
            dispute_payment_event(
                payment_id=transaction.payment.id,
                dispute_tracking_id=dispute.dispute_tracking_id,
            )

        return {
            "transaction": transaction,
            "reason_type": data["reason_type"],
            "reason_message": data["reason_message"],
        }

    def _factory_dispute(self, transaction_id, reason_message, reason_type):
        return create_dispute_transaction(
            transaction_id=transaction_id,
            reason_message=reason_message,
            reason_type=reason_type,
        )
