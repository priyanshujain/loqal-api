from django.utils.translation import gettext as _

from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (create_merchant_code_protocols,
                                 get_merchant_code_protocols,
                                 update_merchant_code_protocols)
from apps.merchant.validators import CodesAndProtocolsValidator

__all__ = ("UpdateCodesAndProtocols",)


class UpdateCodesAndProtocols(ServiceBase):
    def __init__(self, merchant_id, data):
        self.data = data
        self.merchant_id = merchant_id

    def handle(self):
        data = self._validate_data()
        self._update_data(data)

    def _validate_data(self):
        data = run_validator(CodesAndProtocolsValidator, self.data)
        return data

    def _update_data(self, data):
        if get_merchant_code_protocols(merchant_id=self.merchant_id):
            update_merchant_code_protocols(
                merchant_id=self.merchant_id, **data
            )
        else:
            create_merchant_code_protocols(
                merchant_id=self.merchant_id, **data
            )
