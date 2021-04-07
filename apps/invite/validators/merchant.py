from api import serializers

__all__ = (
    "B2CInviteValidator",
    "B2BInviteValidator",
)


class B2CInviteValidator(serializers.ValidationSerializer):
    phone_number = serializers.CharField(max_length=10)
    phone_number_country = serializers.CharField(max_length=2, default="US")
    consumer_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)


class B2BInviteValidator(serializers.ValidationSerializer):
    phone_number = serializers.CharField(max_length=10, required=False)
    phone_number_country = serializers.CharField(max_length=2, default="US")
    merchant_name = serializers.CharField()
    email = serializers.EmailField(required=False)
