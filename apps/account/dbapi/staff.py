from apps.account.models import MerchantAccount

__all__ = ("get_active_merchants", "get_active_non_loqal_merchants")


def get_active_merchants():
    return MerchantAccount.objects.filter(is_active=True)


def get_active_non_loqal_merchants():
    return MerchantAccount.objects.filter(is_active=True, account=None)
