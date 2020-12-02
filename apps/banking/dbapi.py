from apps.provider.lib.api import account
from django.db import IntegrityError

from apps.banking.models import BankAccount


def create_bank_account(
    account_id,
    plaid_access_token,
    plaid_account_id,
    account_number_suffix,
    bank_name,
    bank_logo_base64,
    name,
):
    try:
        return BankAccount.objects.create(
            account_id=account_id,
            plaid_access_token=plaid_access_token,
            plaid_account_id=plaid_account_id,
            account_number_suffix=account_number_suffix,
            bank_name=bank_name,
            bank_logo_base64=bank_logo_base64,
            name=name,
        )
    except IntegrityError:
        return None
