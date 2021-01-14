from django.utils.translation import gettext as _

from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (create_merchant_operation_hour_by_day,
                                 get_merchant_operation_hour_by_day,
                                 update_merchant_operation_hour_by_day)
from apps.merchant.validators import MerchantOperationHoursValidator

__all__ = ("UpdateOperationHours",)


class UpdateOperationHours(ServiceBase):
    def __init__(self, merchant_id, data):
        self.data = data
        self.merchant_id = merchant_id

    def handle(self):
        self.data = self._validate_data()
        for oh_day in self.data:
            self._update_operation_hours(oh_day)

    def _validate_data(self):
        data = run_validator(
            MerchantOperationHoursValidator, self.data, many=True
        )
        return data

    def _update_operation_hours(self, oh_day):
        if get_merchant_operation_hour_by_day(
            merchant_id=self.merchant_id, day=oh_day["day"]
        ):
            update_merchant_operation_hour_by_day(
                merchant_id=self.merchant_id, **oh_day
            )
        else:
            create_merchant_operation_hour_by_day(
                merchant_id=self.merchant_id, **oh_day
            )
