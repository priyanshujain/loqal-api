from api import serializers

__all__ = ("PhoneNumberValidator",)


class PhoneNumberValidator(serializers.ValidationSerializer):
    # Add a phone_number validator
    phone_number = serializers.CharField(max_length=10)
