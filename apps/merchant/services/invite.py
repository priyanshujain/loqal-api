from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.account.dbapi import get_consumer_account_by_phone_number

__all__ = ("InviteConsumerBySMS",)


class InviteConsumerBySMS(ServiceBase):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def handle(self):
        consumer = get_consumer_account_by_phone_number(
            phone_number=self.phone_number
        )
        if consumer:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("The user already exists on Loqal App.")
                    )
                }
            )
