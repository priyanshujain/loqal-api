from api import serializers
from apps.notification.models import (StaffPaymentNotificationSetting,
                                      UserDevice)
from apps.notification.options import PaymentNotificationTypes, UserDeviceTypes

__all__ = (
    "RegisterUserDeviceValidator",
    "UnSubscribeUserDeviceValidator",
    "CreateStaffPaymentNotificationSettingValidator",
    "DisableStaffPaymentNotificationSettingValidator",
    "DeleteStaffPaymentNotificationSettingValidator",
)


class RegisterUserDeviceValidator(serializers.ModelSerializer):
    device_platform = serializers.EnumChoiceField(enum_type=UserDeviceTypes)
    device_id = serializers.CharField()

    class Meta:
        model = UserDevice
        fields = (
            "device_name",
            "device_id",
            "build_number",
            "brand_name",
            "api_level",
            "fcm_token",
            "device_platform",
            "manufacturer",
        )


class UnSubscribeUserDeviceValidator(serializers.ModelSerializer):
    device_id = serializers.CharField()

    class Meta:
        model = UserDevice
        fields = ("device_id",)


class CreateStaffPaymentNotificationSettingValidator(
    serializers.ValidationSerializer
):
    notification_type = serializers.EnumChoiceField(
        enum_type=PaymentNotificationTypes
    )
    staff_id = serializers.IntegerField()
    sms_enabled = serializers.BooleanField()
    email_enabled = serializers.BooleanField()


class DisableStaffPaymentNotificationSettingValidator(
    serializers.ModelSerializer
):
    class Meta:
        model = StaffPaymentNotificationSetting
        fields = ("setting_id",)


class DeleteStaffPaymentNotificationSettingValidator(
    serializers.ModelSerializer
):
    class Meta:
        model = StaffPaymentNotificationSetting
        fields = ("setting_id",)
