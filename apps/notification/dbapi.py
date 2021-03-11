import re

from django.db.utils import IntegrityError
from rest_framework.utils.formatting import remove_trailing_string

from apps.notification.models import (StaffPaymentNotificationSetting,
                                      UserDevice)


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
        return UserDevice.objects.get(user_id=user_id, device_id=device_id)
    except UserDevice.DoesNotExist:
        return None


def get_active_device_by_id(user_id, device_id):
    try:
        return UserDevice.objects.get(
            user_id=user_id, device_id=device_id, active=True
        )
    except UserDevice.DoesNotExist:
        return None


def get_devices_by_user(user_id):
    return UserDevice.objects.filter(user_id=user_id, active=True)


def create_staff_payment_notification_setting(
    merchant_id,
    notification_type,
    sms_enabled=False,
    email_enabled=False,
    app_enabled=True,
    phone_number="",
    phone_number_country="US",
    email="",
    staff_id=None,
):
    try:
        return StaffPaymentNotificationSetting.objects.create(
            merchant_id=merchant_id,
            notification_type=notification_type,
            sms_enabled=sms_enabled,
            email_enabled=email_enabled,
            app_enabled=app_enabled,
            phone_number=phone_number,
            phone_number_country=phone_number_country,
            email=email,
            staff_id=staff_id,
        )
    except IntegrityError:
        return None


def update_staff_payment_notification_setting(
    setting_id,
    notification_type,
    sms_enabled=False,
    email_enabled=False,
    app_enabled=True,
    phone_number="",
    phone_number_country="US",
    email="",
    staff_id=None,
):
    return StaffPaymentNotificationSetting.objects.filter(
        id=setting_id
    ).update(
        notification_type=notification_type,
        sms_enabled=sms_enabled,
        email_enabled=email_enabled,
        app_enabled=app_enabled,
        phone_number=phone_number,
        phone_number_country=phone_number_country,
        email=email,
        staff_id=staff_id,
    )


def get_all_staff_payment_notification_setting(
    merchant_id,
):
    return StaffPaymentNotificationSetting.objects.filter(
        merchant_id=merchant_id
    )


def get_staff_payment_notification_setting(
    merchant_id,
    setting_id,
):
    notification_settings = StaffPaymentNotificationSetting.objects.filter(
        merchant_id=merchant_id, u_id=setting_id
    )
    if notification_settings.exists():
        return notification_settings.first()
    return None


def get_staff_payment_notification_setting_by_staff(
    merchant_id,
    staff_id,
):
    notification_settings = StaffPaymentNotificationSetting.objects.filter(
        merchant_id=merchant_id, staff_id=staff_id
    )
    if notification_settings.exists():
        return notification_settings.first()
    return None


def get_staff_payment_notifications(merchant_id):
    return StaffPaymentNotificationSetting.objects.filter(
        merchant_id=merchant_id, is_active=True
    )
