from api import serializers
from apps.provider.models import PaymentProvider, TermsDocument


class TermsDocumentResponse(serializers.ModelSerializer):
    class Meta:
        model = TermsDocument
        fields = "__all__"


class PaymentProviderResponse(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = "__all__"
