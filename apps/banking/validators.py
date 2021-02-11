from api import serializers

__all__ = ("CreateBankAccountValidator",)


class CreateBankAccountValidator(serializers.ValidationSerializer):
    plaid_public_token = serializers.CharField(max_length=128)
    plaid_account_id = serializers.CharField(max_length=256)


class ReauthBankAccountValidator(serializers.ValidationSerializer):
    plaid_public_token = serializers.CharField(max_length=128)


class CreateIAVBankAccountValidator(serializers.ValidationSerializer):
    funding_source_url = serializers.URLField(max_length=256)
