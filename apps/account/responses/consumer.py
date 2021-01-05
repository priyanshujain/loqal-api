from api import serializers
from apps.account.dbapi import get_payment_account_consent
from apps.account.models import ConsumerAccount

__all__ = ("ConsumerAccountProfileResponse",)


class ConsumerAccountProfileResponse(serializers.ModelSerializer):
    zip_code = serializers.CharField(source="account.zip_code", read_only=True)
    payment_account_opening_consent = serializers.SerializerMethodField(
        "get_payment_account_opening_consent"
    )

    class Meta:
        model = ConsumerAccount
        fields = (
            "created_at",
            "zip_code",
            "username",
            "payment_account_opening_consent",
        )

    def get_payment_account_opening_consent(self, obj):
        consent = get_payment_account_consent(
            account_id=obj.account.id, user_id=obj.account.id
        )
        if consent:
            return True
        return False
