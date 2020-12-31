"""
Validators for consumer APIs
"""
from api import serializers
from apps.notification.options import UserDeviceTypes
from lib.auth import password_validation

__all__ = (
    "CreateConsumerAccountValidator",
    "ConsumerZipCodeValidator",
    "ConsumerUsernameValidator",
)


class CreateConsumerAccountValidator(serializers.ValidationSerializer):
    """
    Validate consumer account
    """

    first_name = serializers.CharField(max_length=512)
    last_name = serializers.CharField(max_length=512)
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=64)
    user_device_type = serializers.ChoiceField(choices=UserDeviceTypes.choices)
    device_registration_id = serializers.CharField(max_length=128)

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password


class ConsumerZipCodeValidator(serializers.ValidationSerializer):
    """
    Validate consumer account zipcode
    """

    # TODO: Add a validator for 5 digit code
    zip_code = serializers.CharField(max_length=5)


class ConsumerUsernameValidator(serializers.ValidationSerializer):
    """
    check consumer account username
    """

    username = serializers.CharField(max_length=32)
