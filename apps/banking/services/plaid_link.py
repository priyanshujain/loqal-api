from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from plugins.plaid import PlaidPlugin


__all__ = (
    "PlaidLink",
)

class PlaidLink(object):
    _token = None

    def __init__(self, account_uid):
        self.account_uid = account_uid

    def generate_token(self):
        plaid = PlaidPlugin()
        link_token = plaid.create_link_token(
            user_account_id=self.account_uid
        )
        if not link_token:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Internal error please try again.")
                    )
                }
            )
        return link_token

    @property
    def token(self):
        if self._token:
            return self._token
        return self.generate_token()
