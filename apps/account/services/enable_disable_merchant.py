from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import get_merchant_account_by_uid
from apps.account.validators import EnableDisableMerchantValidator

__all__ = (
    "DisableMerchant",
    "EnableMerchant",
)


class DisableMerchant(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        self._validate_data()
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=self.merchant_id
        )
        if not merchant_account.is_active:
            raise ValidationError(
                {"detail": ErrorDetail(_("Merchant is already disabled."))}
            )
        merchant_account.deactivate()
        return merchant_account

    def _validate_data(self):
        data = run_validator(EnableDisableMerchantValidator, self.data)
        self.merchant_id = data["merchant_id"]


class EnableMerchant(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        self._validate_data()
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=self.merchant_id
        )
        if merchant_account.is_active:
            raise ValidationError(
                {"detail": ErrorDetail(_("Merchant is already active."))}
            )
        merchant_account.activate()
        return merchant_account

    def _validate_data(self):
        data = run_validator(EnableDisableMerchantValidator, self.data)
        self.merchant_id = data["merchant_id"]
