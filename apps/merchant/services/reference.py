from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException
from apps.provider.lib.actions import ProviderAPIActionBase

__all__ = ("BusinessClassifications",)


class BusinessClassifications(object):
    def __init__(self, account_id):
        self.account_id = account_id

    def get(self):
        psp_response = ProviderAPIAction(
            account_id=self.account_id
        ).get_business_classifcations()
        return psp_response["data"]


class ProviderAPIAction(ProviderAPIActionBase):
    def get_business_classifcations(self):
        response = self.client.reference.business_classifcations()
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
            "status": response.get("status"),
            "data": response.get("data"),
        }
