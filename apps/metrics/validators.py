from api import serializers

__all__ = (
    "CreateSocialShareValidator",
    "CreateMerchantToConsumerRatingValidator",
)


class CreateSocialShareValidator(serializers.ValidationSerializer):
    transaction_id = serializers.CharField(max_length=128)
    platform = serializers.CharField(max_length=256)
    content = serializers.CharField(max_length=2 * 1024)


class CreateMerchantToConsumerRatingValidator(
    serializers.ValidationSerializer
):
    transaction_id = serializers.CharField(max_length=128)
