from django.db.utils import IntegrityError

from apps.account.models import MerchantAccount
from apps.merchant.models import (CodesAndProtocols, MerchantCategory,
                                  MerchantOperationHours, MerchantProfile,
                                  ServiceAvailability, StoreImage)

__all__ = (
    "create_merchant_profile",
    "update_merchant_profile",
    "get_merchants_by_category",
    "get_merchant_operation_hours",
    "update_merchant_operation_hour_by_day",
    "get_merchant_operation_hour_by_day",
    "create_merchant_operation_hour_by_day",
    "get_merchant_code_protocols",
    "update_merchant_code_protocols",
    "create_merchant_code_protocols",
    "get_merchant_service_availability",
    "update_merchant_service_availability",
    "create_merchant_service_availability",
    "get_merchant_category_by_name",
    "create_merchant_category",
    "update_merchant_category",
    "get_merchant_category_by_merchant",
    "create_store_image",
    "get_store_image",
)


def create_merchant_profile(
    merchant_id, name, address, category, sub_category, phone_number
):
    try:
        profile = MerchantProfile.objects.create(
            merchant_id=merchant_id,
            full_name=name,
            address=address,
            phone_number=phone_number,
        )
        MerchantCategory.objects.create(
            merchant_id=merchant_id,
            category=category,
            is_primary=True,
            sub_categories=[sub_category],
        )
        return profile
    except IntegrityError:
        return None


def update_merchant_profile(
    merchant_id,
    about,
    full_name,
    address,
    background_file_id=None,
    avatar_file_id=None,
    website="",
    facebook_page="",
    instagram_page="",
    youtube_page="",
    yelp_page="",
    phone_number="",
    parking_details="",
    dress_code="",
    dining_styles=[],
    cuisines=[],
    amenities=[],
    additional_details="",
):
    """
    Update merchant profile
    """
    MerchantProfile.objects.filter(merchant_id=merchant_id).update(
        about=about,
        full_name=full_name,
        address=address,
        background_file_id=background_file_id,
        avatar_file_id=avatar_file_id,
        website=website,
        facebook_page=facebook_page,
        instagram_page=instagram_page,
        youtube_page=youtube_page,
        yelp_page=yelp_page,
        phone_number=phone_number,
        parking_details=parking_details,
        dress_code=dress_code,
        dining_styles=dining_styles,
        cuisines=cuisines,
        amenities=amenities,
        additional_details=additional_details,
    )


def get_merchants_by_category(category):
    return MerchantAccount.objects.filter(
        account__is_active=True, categories__category=category
    )


def get_merchant_operation_hours(merchant_id):
    return MerchantOperationHours.objects.filter(merchant_id=merchant_id)


def get_merchant_operation_hour_by_day(merchant_id, day):
    try:
        return MerchantOperationHours.objects.get(
            merchant_id=merchant_id, day=day
        )
    except MerchantOperationHours.DoesNotExist:
        return None


def update_merchant_operation_hour_by_day(
    merchant_id, day, open_time, close_time, is_closed
):
    return MerchantOperationHours.objects.filter(
        merchant_id=merchant_id, day=day
    ).update(open_time=open_time, close_time=close_time, is_closed=is_closed)


def create_merchant_operation_hour_by_day(
    merchant_id, day, open_time, close_time, is_closed
):
    try:
        return MerchantOperationHours.objects.create(
            merchant_id=merchant_id,
            day=day,
            open_time=open_time,
            close_time=close_time,
            is_closed=is_closed,
        )
    except IntegrityError:
        return True


def get_merchant_code_protocols(merchant_id):
    try:
        return CodesAndProtocols.objects.get(merchant_id=merchant_id)
    except CodesAndProtocols.DoesNotExist:
        return None


def update_merchant_code_protocols(
    merchant_id,
    mask_required,
    sanitizer_provided,
    outdoor_seating,
    cleaning_frequency,
    last_cleaned_at,
):
    return CodesAndProtocols.objects.filter(merchant_id=merchant_id).update(
        mask_required=mask_required,
        sanitizer_provided=sanitizer_provided,
        outdoor_seating=outdoor_seating,
        cleaning_frequency=cleaning_frequency,
        last_cleaned_at=last_cleaned_at,
    )


def create_merchant_code_protocols(
    merchant_id,
    mask_required,
    sanitizer_provided,
    outdoor_seating,
    cleaning_frequency,
    last_cleaned_at,
):
    try:
        return CodesAndProtocols.objects.create(
            merchant_id=merchant_id,
            mask_required=mask_required,
            sanitizer_provided=sanitizer_provided,
            outdoor_seating=outdoor_seating,
            cleaning_frequency=cleaning_frequency,
            last_cleaned_at=last_cleaned_at,
        )
    except IntegrityError:
        return True


def get_merchant_service_availability(merchant_id):
    try:
        return ServiceAvailability.objects.get(merchant_id=merchant_id)
    except ServiceAvailability.DoesNotExist:
        return None


def update_merchant_service_availability(
    merchant_id,
    curbside_pickup,
    delivery,
    takeout,
    sitting_dining,
):
    return ServiceAvailability.objects.filter(merchant_id=merchant_id).update(
        curbside_pickup=curbside_pickup,
        delivery=delivery,
        takeout=takeout,
        sitting_dining=sitting_dining,
    )


def create_merchant_service_availability(
    merchant_id,
    curbside_pickup,
    delivery,
    takeout,
    sitting_dining,
):
    try:
        return ServiceAvailability.objects.create(
            merchant_id=merchant_id,
            curbside_pickup=curbside_pickup,
            delivery=delivery,
            takeout=takeout,
            sitting_dining=sitting_dining,
        )
    except IntegrityError:
        return True


def get_merchant_category_by_name(merchant_id, category):
    try:
        return MerchantCategory.objects.get(
            merchant_id=merchant_id, category=category
        )
    except MerchantCategory.DoesNotExist:
        return None


def get_merchant_category_by_merchant(merchant_id):
    return MerchantCategory.objects.filter(merchant_id=merchant_id)


def create_merchant_category(
    merchant_id, category, sub_categories, is_primary=False
):
    if is_primary:
        MerchantCategory.objects.filter(merchant_id=merchant_id).update(
            is_primary=False
        )
    try:
        return MerchantCategory.objects.create(
            merchant_id=merchant_id,
            category=category,
            sub_categories=sub_categories,
            is_primary=is_primary,
        )
    except IntegrityError:
        return None


def update_merchant_category(
    merchant_id, category, sub_categories, is_primary=False
):
    if is_primary:
        MerchantCategory.objects.filter(merchant_id=merchant_id).update(
            is_primary=False
        )
    return MerchantCategory.objects.filter(
        merchant_id=merchant_id, category=category
    ).update(sub_categories=sub_categories, is_primary=is_primary)


def create_store_image(merchant_id, image, alt=""):
    try:
        return StoreImage.objects.create(
            merchant_id=merchant_id, image=image, alt=alt
        )
    except IntegrityError:
        return None


def get_store_image(merchant_id, image_id):
    try:
        return StoreImage.objects.get(merchant_id=merchant_id, u_id=image_id)
    except StoreImage.DoesNotExist:
        return None
