from api import serializers
from apps.banking.models import BankAccount

__all__ = ("BankAccountResponse",)


class BankAccountResponse(serializers.ModelSerializer):
    status = serializers.ChoiceCharEnumSerializer(
        source="dwolla_funding_source_status", read_only=True
    )

    class Meta:
        model = BankAccount
        fields = (
            "id",
            "account_number_suffix",
            "bank_name",
            "bank_logo_base64",
            "is_disabled",
            "currency",
            "created_at",
            "name",
            "status",
        )
