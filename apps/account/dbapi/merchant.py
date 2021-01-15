from django.db.utils import IntegrityError

from apps.account.models import Account, MerchantAccount

__all__ = (
    "create_merchant_account",
    "get_merchant_account",
    "get_merchant_account_by_uid",
    "create_non_loqal_merchant_account",
)


def create_merchant_account(company_email):
    account = Account.objects.create()
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


def get_merchant_account_by_uid(merchant_uid):
    try:
        return MerchantAccount.objects.get(u_id=merchant_uid)
    except MerchantAccount.DoesNotExist:
        return None
