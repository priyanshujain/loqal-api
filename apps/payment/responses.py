from api import serializers
from apps.payment.models import Transaction, models

__all__ = ("TransactionResponse",)


class TransactionResponse(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField(source="recipient.id", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "recipient_id",
            "payment_amount",
            "payment_currency",
            "status",
        )
