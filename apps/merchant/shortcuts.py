from apps.merchant.constants import MERCHANT_CATEGORIES


def validate_subcategory(category, sub_category):
    for merchant_category in MERCHANT_CATEGORIES:
        if merchant_category["category_slug"] == category:
            for merchant_sub_category in merchant_category["subcategories"]:
                if merchant_sub_category["slug"] == sub_category:
                    return True
            return False
    return False


def validate_category(category):
    for merchant_category in MERCHANT_CATEGORIES:
        if merchant_category["category_slug"] == category:
            return True
    return False
