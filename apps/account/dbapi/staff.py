from apps.account.models import MerchantAccount

__all__ = ("get_loqal_merchants", "get_active_non_loqal_merchants")


def get_loqal_merchants():
    return MerchantAccount.objects.filter(account__isnull=False)


def get_active_non_loqal_merchants():
    return MerchantAccount.objects.filter(account=None)
