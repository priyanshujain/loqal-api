import json

from django import forms

from api import serializers
from apps.provider.models import (PaymentProvider, PaymentProviderCred,
                                  TermsDocument)
from apps.provider.options import TermsDocumentTypes
from integrations.options import IntegratedProviders


class CreatePaymentProviderSerializer(serializers.ValidationSerializer):
    """Validate new payment provider object"""

    provider_slug = serializers.ChoiceField(
        choices=IntegratedProviders.choices()
    )
    display_name = serializers.CharField(max_length=255)
    website = serializers.URLField()


class UpdatePaymentProviderSerializer(CreatePaymentProviderSerializer):
    """Validate existing payment provider object for update"""

    paymentprovider_id = serializers.IntegerField()


class PaymentProviderModelSerializer(serializers.ModelSerializer):
    """Model serializer for payment provider"""

    class Meta:
        model = PaymentProvider
        fields = "__all__"


class ProviderLogoUploadForm(forms.Form):
    """Validate logo file"""

    logo = forms.FileField()
    paymentprovider_id = forms.IntegerField()


class PaymentProviderCredSerializer(serializers.ValidationSerializer):
    """Validate payment provider credentials fields"""

    provider_id = serializers.IntegerField()
    api_environment = serializers.CharField(max_length=255)
    api_password = serializers.CharField(max_length=255)
    api_key = serializers.CharField(max_length=255)
    api_login_id = serializers.CharField(max_length=255)


class CreateTermsDocumentSerializer(serializers.ValidationSerializer):
    """Create term document serializer"""

    provider_id = serializers.IntegerField()
    document_type = serializers.ChoiceField(
        choices=TermsDocumentTypes.choices()
    )
    document_file = serializers.JSONField()
    is_active = serializers.BooleanField(default=True)
    country = serializers.CharField(max_length=2)


class RemoveTermDocumentSerializer(serializers.ValidationSerializer):
    """remove terms document, validate id"""

    termdocument_id = serializers.IntegerField()


class ActivateTermDocumentSerializer(serializers.ValidationSerializer):
    """activate terms document, validate id"""

    termdocument_id = serializers.IntegerField()


class PaymentProviderSerializer(serializers.ModelSerializer):
    provider_slug = serializers.ChoiceField(
        choices=IntegratedProviders.choices()
    )

    class Meta:
        model = PaymentProvider
        fields = "__all__"


class TermsDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsDocument
        fields = "__all__"


class PaymentProviderCredModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProviderCred
        fields = "__all__"
