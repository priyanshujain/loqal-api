from apps.account.models import MerchantAccount

__all__ = ("get_active_merchants",)


def get_active_merchants():
    return MerchantAccount.objects.filter(is_active=True)
