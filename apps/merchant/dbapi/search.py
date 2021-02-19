from django.db.models import Q

from apps.account.models import MerchantAccount


def get_all_merchants():
    return MerchantAccount.objects.filter(
        Q(account__is_active=True) | Q(account=None)
    )


def get_merchant_qs_by_category(category, merchant_qs=None):
    if not merchant_qs:
        merchant_qs = get_all_merchants()
    return merchant_qs.filter(categories__category=category)


def merchant_search_by_keyword(merchant_qs, keyword):
    category_keyword = keyword.replace(" ", "_").replace("-", "_")
    sub_category_keyword = keyword.replace(" ", "-").replace("_", "-")
    return merchant_qs.filter(
        Q(profile__full_name__icontains=keyword)
        | Q(categories__category__icontains=category_keyword)
        | Q(profile__about__icontains=keyword)
        | Q(categories__sub_categories__icontains=sub_category_keyword)
    ).distinct()
