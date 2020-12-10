from django.db.utils import IntegrityError

from apps.account.models import Account, MerchantAccount

__all__ = (
    "create_merchant_account",
    "get_merchant_account",
)


def create_merchant_account(company_name, company_email):
    account = Account.objects.create()
    try:
        return MerchantAccount.objects.create(
            account=account, company_name=company_name, company_email=company_email
        )
    except IntegrityError:
        account.delete()
        return None


def get_merchant_account(account_id):
    try:
        return MerchantAccount.objects.get(account_id=account_id)
    except MerchantAccount.DoesNotExist:
        return None
