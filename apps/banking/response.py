from api import serializers
from apps.banking.models import BankAccount

__all__ = ("BankAccountResponse",)


class BankAccountResponse(serializers.ModelSerializer):
    status = serializers.ChoiceCharEnumSerializer(
        source="dwolla_funding_source_status", read_only=True
    )
    plaid_status = serializers.ChoiceCharEnumSerializer(read_only=True)
    bank_account_id = serializers.CharField(source="u_id", read_only=True)

    class Meta:
        model = BankAccount
        fields = (
            "bank_account_id",
            "account_number_suffix",
            "bank_name",
            "bank_logo_base64",
            "is_disabled",
            "currency",
            "created_at",
            "name",
            "status",
            "plaid_status",
        )
