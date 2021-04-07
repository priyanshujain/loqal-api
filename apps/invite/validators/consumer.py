from logging import FATAL

from api import serializers

__all__ = (
    "C2CInviteValidator",
    "C2BInviteValidator",
    "PhoneNumberListValidator",
)


class C2CInviteValidator(serializers.ValidationSerializer):
    phone_number = serializers.CharField(max_length=10)
    phone_number_country = serializers.CharField(max_length=2, default="US")
    consumer_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)


class C2BInviteValidator(serializers.ValidationSerializer):
    phone_number = serializers.CharField(max_length=10, required=False)
    phone_number_country = serializers.CharField(max_length=2, default="US")
    merchant_name = serializers.CharField()
    email = serializers.EmailField(required=False)


class PhoneNumberListValidator(serializers.ValidationSerializer):
    # Add a phone_number validator
    phone_numbers = serializers.ListField(
        child=serializers.CharField(max_length=10),
        allow_empty=True,
        default=[],
    )
