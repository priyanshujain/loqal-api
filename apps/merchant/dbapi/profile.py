from django.db.utils import IntegrityError

from apps.merchant.models import MerchantProfile

__all__ = (
    "create_merchant_profile",
    "update_merchant_profile",
)


def create_merchant_profile(
    merchant_id, name, address, category, sub_category, phone_number
):
    try:
        return MerchantProfile.objects.create(
            merchant_id=merchant_id,
            full_name=name,
            address=address,
            category=category,
            sub_category=sub_category,
            phone_number=phone_number,
        )
    except IntegrityError:
        return None


def update_merchant_profile(
    merchant_id,
    about,
    full_name,
    address,
    category,
    sub_category,
    hero_image=None,
    neighborhood="",
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
        category=category,
        sub_category=sub_category,
        hero_image=hero_image,
        neighborhood=neighborhood,
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
