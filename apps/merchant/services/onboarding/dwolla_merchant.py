from apps.provider.lib.api import account
from api.helpers import run_validator
from apps.account.dbapi import get_merchant_account, merchant
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException
from api.services import ServiceBase
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.merchant.validators import OnboardingDataValidator
from apps.merchant.serializers import OnboardingDataSerializer
from apps.merchant.dbapi import get_account_member_by_user_id
from integrations.utils.options import RequestStatusTypes


__all__ = ("CreateDwollaMerchantAccount",)


class CreateDwollaMerchantAccount(ServiceBase):
    def __init__(self, merchant_id, user_id, ip_address):
        self.merchant_id = merchant_id
        self.user_id = user_id
        self.ip_address = ip_address

    def handle(self):
        data, merchant = self._prepare_data()
        return self._create_dwolla_acconut(data=data, merchant=merchant)
    
    def _prepare_data(self):
        merchant = get_merchant_account(merchant_id=self.merchant_id)
        data = OnboardingDataSerializer(merchant).data
        assert self._validate_data(data=data)
        merchant_member = get_account_member_by_user_id(user_id=self.user_id)
        data["incorporation_details"]["user"] = {
            "first_name": merchant_member.user.first_name,
            "last_name": merchant_member.user.last_name,
            "email": merchant_member.user.email,
        }
        data["incorporation_details"]["ip_address"] = self.ip_address
        return data, merchant
    
    def _validate_data(self, data):
        run_validator(validator=OnboardingDataValidator, data=data)
        return True

    def _create_dwolla_acconut(self, data, merchant):
        account = merchant.account
        dwolla_response = DwollaCreateMerchantAccountAPIAction(account_id=account.id).create(data=data)
        account.add_dwolla_id(dwolla_id=dwolla_response["dwolla_customer_id"])
        merchant.update_status(status=dwolla_response["status"])

class DwollaCreateMerchantAccountAPIAction(ProviderAPIActionBase):
    def create(self, data):
        response = self.client.account.create_merchant_account(data=data)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return {
            "status": response["data"].get("status"),
            "dwolla_customer_id": response["data"]["dwolla_customer_id"],
            "status": response["data"]["status"],
        }