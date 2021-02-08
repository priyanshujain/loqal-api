from math import asin, cos, radians, sin, sqrt

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


def validate_profile_image_type(content_type):
    return "image" in content_type


def coordinate_distance(lat1, lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth
    # r = 6371 # For KMs
    r = 3956  # For miles

    # calculate the result
    return c * r
