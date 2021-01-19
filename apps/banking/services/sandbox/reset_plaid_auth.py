from django.utils.translation import gettext as _
from api.exceptions import ErrorDetail, ValidationError

from plugins.plaid import PlaidPlugin
from plugins.plaid.errors import PlaidReAuth


class ResetPlaidLogin(object):
    def __init__(self, bank_account):
        self.bank_account = bank_account

    def handle(self):
        plaid = PlaidPlugin()
        try:
            plaid.sandbox_reset_login(access_token=self.bank_account.plaid_access_token)
        except PlaidReAuth:
            raise ValidationError(
                {"detail": [ErrorDetail("Plaid account is already in reset state.")]}
            )
