from api import serializers
from apps.account.responses import MerchantDetailsResponse
from apps.payment.models import Transaction, models

__all__ = ("TransactionResponse",)


class TransactionResponse(serializers.ModelSerializer):
    merchant = MerchantDetailsResponse(
        source="recipient.account.merchantaccount", read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "created_at",
            "merchant",
            "payment_amount",
            "tip_amount",
            "payment_currency",
            "status",
        )
