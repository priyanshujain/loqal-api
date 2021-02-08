from django.db.utils import IntegrityError

from apps.account.models import Account, MerchantAccount

__all__ = (
    "create_merchant_account",
    "get_merchant_account",
    "get_merchant_account_by_uid",
    "create_non_loqal_merchant_account",
    "get_account_by_id",
)


def create_merchant_account(company_email):
    # FIX: Move it to webhooks when onoboarding marks it verified
    account = Account.objects.create(is_verified_dwolla_customer=True)
    try:
        return MerchantAccount.objects.create(
            account=account,
            company_email=company_email,
        )
    except IntegrityError:
        account.delete()
        return None


def create_non_loqal_merchant_account():
    return MerchantAccount.objects.create()


def get_merchant_account(merchant_id):
    try:
        return MerchantAccount.objects.get(id=merchant_id)
    except MerchantAccount.DoesNotExist:
        return None


def get_account_by_id(account_id):
    try:
        return Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return None


def get_merchant_account_by_uid(merchant_uid):
    try:
        return MerchantAccount.objects.get(u_id=merchant_uid)
    except MerchantAccount.DoesNotExist:
        return None
