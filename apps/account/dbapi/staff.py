from apps.account.models import ConsumerAccount, MerchantAccount

__all__ = (
    "get_loqal_merchants",
    "get_active_non_loqal_merchants",
    "get_loqal_consumers",
)


def get_loqal_merchants():
    return MerchantAccount.objects.filter(account__isnull=False)


def get_loqal_consumers():
    return ConsumerAccount.objects.filter(account__isnull=False)


def get_active_non_loqal_merchants():
    return MerchantAccount.objects.filter(account=None)
