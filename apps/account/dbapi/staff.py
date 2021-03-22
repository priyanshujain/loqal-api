from apps.account.models import ConsumerAccount, MerchantAccount

__all__ = (
    "get_loqal_merchants",
    "get_active_non_loqal_merchants",
    "get_loqal_consumers",
    "get_loqal_consumer",
)


def get_loqal_merchants():
    return MerchantAccount.objects.filter(account__isnull=False)


def get_loqal_consumers():
    return ConsumerAccount.objects.filter(account__isnull=False)


def get_loqal_consumer(consumer_id):
    try:
        return ConsumerAccount.objects.get(
            u_id=consumer_id, account__isnull=False
        )
    except ConsumerAccount.DoesNotExist:
        return None


def get_active_non_loqal_merchants():
    return MerchantAccount.objects.filter(account=None)
