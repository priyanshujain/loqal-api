from django.utils.translation import gettext as _
from rest_framework.fields import BooleanField

from api.exceptions import ErrorDetail, ValidationError
from plugins.plaid import PlaidPlugin
from plugins.plaid.errors import PlaidBankUsernameExpired, PlaidReAuth

__all__ = ("CheckBankBalance",)


class CheckBankBalance(object):
    def __init__(self, bank_account):
        self.bank_account = bank_account

    def validate(self):
        bank_account = self.bank_account
        try:
            balance = self._check_balance(bank_account=bank_account)
        except PlaidReAuth:
            bank_account.set_reverification()
            return None, ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Bank account access expired, please re-authenticate your bank account."
                        )
                    ),
                    "code": "PLAID_REVERIFICATION_REQUIRED",
                }
            )
        except PlaidBankUsernameExpired:
            bank_account.set_username_changed()
            return None, ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Bank account user expired, please "
                            "contact your bank or our support team for further assitance."
                        )
                    ),
                    "code": "BANK_USERNAME_CHANGED",
                }
            )
        except ValidationError as err:
            return None, err

        return balance, None

    def _check_balance(self, bank_account):
        plaid = PlaidPlugin()
        balance = plaid.get_balance(
            access_token=bank_account.plaid_access_token,
            account_id=bank_account.plaid_account_id,
        )
        if balance is None:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Balance check failed, please try again.")
                    )
                }
            )
        return balance
