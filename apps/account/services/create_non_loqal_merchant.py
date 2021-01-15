from django.utils.translation import gettext as _

from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import create_non_loqal_merchant_account
from apps.account.validators import CreateNonLoqalMerchantValidator
from apps.merchant.dbapi import create_merchant_profile

__all__ = ("CreateNonLoqalMerchant",)


class CreateNonLoqalMerchant(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        self._validate_data()
        merchant_account = self._factory_merchant_account()
        return merchant_account

    def _validate_data(self):
        data = run_validator(CreateNonLoqalMerchantValidator, self.data)
        self._company_name = data["company_name"]
        self._address = data["address"]
        self._category = data["category"]
        self._sub_category = data["sub_category"]
        self._contact_number = data["phone_number"]

    def _factory_merchant_account(self):
        merchant_account = create_non_loqal_merchant_account()
        create_merchant_profile(
            merchant_id=merchant_account.id,
            name=self._company_name,
            address=self._address,
            category=self._category,
            sub_category=self._sub_category,
            phone_number=self._contact_number,
        )
        return merchant_account
