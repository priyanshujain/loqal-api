from api import serializers
from apps.merchant.models import AccountMember
from apps.notification.models import (StaffPaymentNotificationSetting,
                                      UserDevice)


class RegisterUserDeviceResponse(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = (
            "device_name",
            "device_id",
            "device_tracking_id",
        )


class StaffMemberResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    phone_number = serializers.CharField(
        source="user.phone_number", read_only=True
    )
    phone_number_country = serializers.CharField(
        source="user.phone_number_country", read_only=True
    )

    class Meta:
        model = AccountMember
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "phone_number_country",
        )


class StaffPaymentNotificationSettingResponse(serializers.ModelSerializer):
    notification_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    staff = StaffMemberResponse(read_only=True)
    setting_id = serializers.CharField(source="u_id", read_only=True)

    class Meta:
        model = StaffPaymentNotificationSetting
        fields = (
            "notification_type",
            "staff",
            "sms_enabled",
            "email_enabled",
            "app_enabled",
            "is_active",
            "setting_id",
        )
