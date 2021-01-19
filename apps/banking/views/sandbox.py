from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView, MerchantAPIView
from apps.banking.dbapi import get_bank_account
from apps.banking.services import ResetPlaidLogin


class ConsumerReAuthBankAccountAPI(ConsumerAPIView):
    def post(self, request):
        account = request.account
        bank_account = get_bank_account(account_id=account.id)
        if not bank_account:
            raise ValidationError(
                {"detail": ErrorDetail("Bank account does not exist.")}
            )

        ResetPlaidLogin(bank_account=bank_account).handle()
        return self.response()


class MerchantReAuthBankAccountAPI(MerchantAPIView):
    def post(self, request):
        account = request.account
        bank_account = get_bank_account(account_id=account.id)
        if not bank_account:
            raise ValidationError(
                {"detail": ErrorDetail("Bank account does not exist.")}
            )

        ResetPlaidLogin(bank_account=bank_account).handle()
        return self.response()
