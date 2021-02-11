from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.provider.lib.api import account


class GetIAVToken(ServiceBase):
    def __init__(self, account):
        self.account = account

    def handle(self):
        if not self.account.dwolla_id:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Your account is not allowed to add a bank account.")
                    ),
                }
            )
        api_action = CreateIAVTokenAPIAction(account_id=self.account.id)
        return api_action.get()


class CreateIAVTokenAPIAction(ProviderAPIActionBase):
    def get(self):
        response = self.client.banking.get_iav_token()
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
                            "Your bank account couldn't be verified, Please try "
                            "again later. If the problem persists, please "
                            "contact our support team."
                        )
                    ),
                }
            )
        return response["data"]
