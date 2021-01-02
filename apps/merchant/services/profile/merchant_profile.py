from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, InternalDBError, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import update_merchant_profile
from apps.merchant.validators import MerchantProfileValidator

__all__ = ("UpdateMerchantProfile",)


class UpdateMerchantProfile(ServiceBase):
    def __init__(self, merchant_id, data):
        self.data = data
        self.merchant_id = merchant_id

    def handle(self):
        self.data = self._validate_data()
        self._update_merchant_profile()

    def _validate_data(self):
        data = run_validator(MerchantProfileValidator, self.data)
        return data

    def _update_merchant_profile(self):
        update_merchant_profile(merchant_id=self.merchant_id, **self.data)
