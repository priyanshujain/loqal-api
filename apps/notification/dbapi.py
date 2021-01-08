import re

from django.db.utils import IntegrityError

from apps.notification.models import UserDevice


def register_user_device(
    user_id,
    device_name,
    device_id,
    build_number,
    brand_name,
    api_level,
    fcm_token,
    device_platform,
    manufacturer,
):
    try:
        return UserDevice.objects.create(
            user_id=user_id,
            device_name=device_name,
            device_id=device_id,
            build_number=build_number,
            brand_name=brand_name,
            api_level=api_level,
            fcm_token=fcm_token,
            device_platform=device_platform,
            manufacturer=manufacturer,
        )
    except IntegrityError:
        return None


def get_device_by_id(user_id, device_id):
    try:
        return UserDevice.objects.get(
            user_id=user_id, device_id=device_id, active=True
        )
    except UserDevice.DoesNotExist:
        return None


def get_devices_by_user(user_id):
    return UserDevice.objects.filter(user_id=user_id, active=True)
