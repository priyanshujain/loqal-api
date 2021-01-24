from apps.account.options import DwollaCustomerStatus
from apps.banking.dbapi import get_bank_account


def check_if_merchant_account_ready(merchant):
    account = merchant.account
    if account.dwolla_customer_status != DwollaCustomerStatus.VERIFIED:
        return False
    bank_account = get_bank_account(account_id=account.id)
    if not bank_account.is_payment_allowed():
        return False
    return True
