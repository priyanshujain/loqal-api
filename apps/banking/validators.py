from api import serializers

__all__ = (
    "CreateBankAccountValidator",
    "ReauthBankAccountValidator",
    "CreateIAVBankAccountValidator",
    "VerifyMicroDepositValidator",
)


class CreateBankAccountValidator(serializers.ValidationSerializer):
    plaid_public_token = serializers.CharField(max_length=128)
    plaid_account_id = serializers.CharField(max_length=256)


class ReauthBankAccountValidator(serializers.ValidationSerializer):
    plaid_public_token = serializers.CharField(max_length=128)


class CreateIAVBankAccountValidator(serializers.ValidationSerializer):
    funding_source_url = serializers.URLField(max_length=256)


class VerifyMicroDepositValidator(serializers.ValidationSerializer):
    amount1 = serializers.DecimalField(
        min_value=0,
        max_digits=4,
        decimal_places=2,
        coerce_to_string=False,
    )
    amount2 = serializers.DecimalField(
        min_value=0,
        max_digits=4,
        decimal_places=2,
        coerce_to_string=False,
    )
