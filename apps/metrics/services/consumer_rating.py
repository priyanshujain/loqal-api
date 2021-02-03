from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.metrics.dbapi import create_merchant_to_consumer_rating
from apps.metrics.validators import CreateMerchantToConsumerRatingValidator
from apps.payment.dbapi import get_merchant_transaction


class CreateConsumerRating(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self.validate()
        transaction = data["transaction"]
        return create_merchant_to_consumer_rating(
            consumer_id=transaction.payment.order.consumer.id,
            merchant_id=transaction.payment.order.merchant.id,
            transaction_id=transaction.id,
        )

    def validate(self):
        data = run_validator(CreateMerchantToConsumerRatingValidator, data=self.data)
        transaction_id = data["transaction_id"]
        transaction = get_merchant_transaction(
            merchant_account=self.merchant,
            transaction_tracking_id=transaction_id,
        )
        if not transaction:
            raise ValidationError(
                {"detail": ErrorDetail(_("Transaction is not valid"))}
            )
        data["transaction"] = transaction
        return data
