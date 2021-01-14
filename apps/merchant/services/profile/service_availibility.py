from django.utils.translation import gettext as _

from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (create_merchant_service_availability,
                                 get_merchant_service_availability,
                                 update_merchant_service_availability)
from apps.merchant.validators import ServiceAvailabilityValidator

__all__ = ("UpdateServiceAvailability",)


class UpdateServiceAvailability(ServiceBase):
    def __init__(self, merchant_id, data):
        self.data = data
        self.merchant_id = merchant_id

    def handle(self):
        data = self._validate_data()
        self._update_data(data)

    def _validate_data(self):
        data = run_validator(ServiceAvailabilityValidator, self.data)
        return data

    def _update_data(self, data):
        if get_merchant_service_availability(merchant_id=self.merchant_id):
            update_merchant_service_availability(
                merchant_id=self.merchant_id, **data
            )
        else:
            create_merchant_service_availability(
                merchant_id=self.merchant_id, **data
            )
