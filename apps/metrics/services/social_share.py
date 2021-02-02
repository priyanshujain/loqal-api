from django.utils.translation import TranslatorCommentWarning
from django.utils.translation import gettext as _

from api import services
from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.metrics.dbapi import create_consumer_social_record
from apps.metrics.validators import CreateSocialShareValidator
from apps.payment.dbapi import get_consumer_transaction


class CreateSocialShare(ServiceBase):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    def handle(self):
        data = self.validate()
        return create_consumer_social_record(
            consumer_id=self.consumer.id,
            transaction_id=data["transaction"].id,
            content=data["content"],
            platform=data["platform"],
        )

    def validate(self):
        data = run_validator(CreateSocialShareValidator, data=self.data)
        transaction_id = data["transaction_id"]
        transaction = get_consumer_transaction(
            consumer_account=self.consumer,
            transaction_tracking_id=transaction_id,
        )
        if not transaction:
            raise ValidationError(
                {"detail": ErrorDetail(_("Transaction is not valid"))}
            )
        data["transaction"] = transaction
