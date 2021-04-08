from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.user.dbapi import get_user_by_phone
from apps.user.options import CustomerTypes

__all__ = ("FilterNonLoqalConsumers",)


class FilterNonLoqalConsumers(ServiceBase):
    def __init__(self, phone_numbers):
        self.phone_numbers = phone_numbers

    def handle(self):
        phone_numbers = self._validate_data()
        loqal_phone_numbers = []
        for phone_number in phone_numbers:
            if self.check_user_exists(phone_number=phone_number):
                loqal_phone_numbers.append(phone_number)
        return loqal_phone_numbers

    def _validate_data(self):
        phone_numbers = self.phone_numbers
        if not isinstance(phone_numbers, list):
            raise ValidationError(
                {
                    "phone_numbers": [
                        ErrorDetail(_("It should be a list of phone numbers."))
                    ]
                }
            )

        for phone_number in phone_numbers:
            if not isinstance(phone_number, str) or len(phone_number) != 10:
                raise ValidationError(
                    {
                        "phone_numbers": [
                            ErrorDetail(
                                _("It should be a list of phone numbers.")
                            )
                        ]
                    }
                )
        return phone_numbers

    def check_user_exists(self, phone_number):
        phone_user = get_user_by_phone(
            phone_number=phone_number, customer_type=CustomerTypes.CONSUMER
        )
        if phone_user:
            return True
        else:
            return False
