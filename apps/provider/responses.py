from api import serializers
from apps.provider.models import (PaymentAccount, PaymentAccountOpeningCreds,
                                  PaymentProvider, TermsDocument)


class TermsDocumentResponse(serializers.ModelSerializer):
    class Meta:
        model = TermsDocument
        fields = "__all__"


class PaymentProviderResponse(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = "__all__"


class PaymentAccountResponse(serializers.ModelSerializer):
    provider = PaymentProviderResponse()
    account_number = serializers.PrimaryKeyRelatedField(
        source="account_opening_creds.account_number", read_only=True
    )

    class Meta:
        model = PaymentAccount
        fields = "__all__"
