from django.db.models import Q

from apps.account.models import MerchantAccount


def get_all_merchants():
    return MerchantAccount.objects.filter(is_active=True)


def get_merchant_qs_by_category(merchant_qs, category):
    return merchant_qs.filter(categories__category=category)


def merchant_search_by_keyword(merchant_qs, keyword):
    return merchant_qs.filter(
        Q(profile__full_name__icontains=keyword)
        | Q(categories__category__icontains=keyword)
        | Q(profile__about__icontains=keyword)
    )
