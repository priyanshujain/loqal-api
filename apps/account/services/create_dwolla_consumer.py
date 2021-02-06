from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException
from api.services import ServiceBase
from apps.account.dbapi import get_consumer_account
from apps.provider.lib.actions import ProviderAPIActionBase

__all__ = (
    "CreateConsumerAccount",
    "GenerateUsername",
)


class DwollaConsumerAccount(ServiceBase):
    def __init__(self, user_id, ip_address):
        self.user_id = user_id
        self.ip_address = ip_address

    def handle(self):
        consumer_account = get_consumer_account(user_id=self.user_id)
        return self._create_dwolla_account(consumer_account=consumer_account)

    def _create_dwolla_account(self, consumer_account):
        user = consumer_account.user
        account = consumer_account.account
        psp_req_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "ip_address": self.ip_address,
        }
        psp_action = CreateConsumerAccountAPIAction(account_id=account.id)
        response = psp_action.create(data=psp_req_data)
        dwolla_customer_id = response["dwolla_customer_id"]
        status = response["status"]
        verification_status = response["verification_status"]
        account.add_dwolla_id(dwolla_id=dwolla_customer_id, save=False)
        account.update_status(status=status, verification_status=verification_status)
        return True


class CreateConsumerAccountAPIAction(ProviderAPIActionBase):
    def create(self, data):
        response = self.client.account.create_consumer_account(data=data)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "message": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    ),
                    "detail": ErrorDetail(
                        _(
                            "Your account couldn't be created. "
                            "Please try again in a few hours, or contact our support team."
                        )
                    ),
                }
            )
        return {
            "status": response["data"].get("status"),
            "verification_status": response["data"].get("verification_status"),
            "dwolla_customer_id": response["data"]["dwolla_customer_id"],
        }
