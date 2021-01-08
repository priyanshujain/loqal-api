from api import serializers

__all__ = ("PaymentAccountOpeningConsentValidator",)


class PaymentAccountOpeningConsentValidator(serializers.Serializer):
    consent_timestamp = serializers.IntegerField()
    payment_terms_url = serializers.URLField(max_length=128)
