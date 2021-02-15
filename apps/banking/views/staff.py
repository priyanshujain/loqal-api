from api.exceptions import ErrorDetail, ValidationError
from api.views import StaffAPIView
from apps.account.dbapi import get_account_by_id
from apps.banking.services import SyncBankAccounts


class SyncBankAccountAPI(StaffAPIView):
    def post(self, request, account_id):
        account = get_account_by_id(account_id=account_id)
        if not account or not account.dwolla_id:
            raise ValidationError({"detail": ErrorDetail("Invalid account.")})
        SyncBankAccounts(account=account).handle()
        return self.response()
