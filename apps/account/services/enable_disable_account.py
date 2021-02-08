from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import get_account_by_id
from apps.account.validators import EnableDisableAccountValidator

__all__ = (
    "DisableAccount",
    "EnableAccount",
)


class DisableAccount(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        self._validate_data()
        account = get_account_by_id(account_id=self.account_id)
        if not account.is_active:
            raise ValidationError(
                {"detail": ErrorDetail(_("Account is already disabled."))}
            )
        account.deactivate()
        return account

    def _validate_data(self):
        data = run_validator(EnableDisableAccountValidator, self.data)
        self.account_id = data["account_id"]


class EnableAccount(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        self._validate_data()
        account = get_account_by_id(account_id=self.account_id)
        if account.is_active:
            raise ValidationError(
                {"detail": ErrorDetail(_("Account is already active."))}
            )
        account.activate()
        return account

    def _validate_data(self):
        data = run_validator(EnableDisableAccountValidator, self.data)
        self.account_id = data["account_id"]
