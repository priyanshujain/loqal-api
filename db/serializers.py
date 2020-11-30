# DELETE: delete this file after refactor

from rest_framework import serializers

from utils.choices import Choices


class AddressSerializer(serializers.Serializer):
    address1 = serializers.CharField(max_length=1024)
    address2 = serializers.CharField(
        max_length=1024,
        default="",
        allow_blank=True,
        allow_null=True,
        required=False,
    )
    country = serializers.CharField(max_length=2)
    state = serializers.CharField(max_length=3)
    city = serializers.CharField(max_length=255, required=False)
    zip_code = serializers.CharField(max_length=10)


class PaymentAccountBaseSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=50)
    currency = serializers.CharField(max_length=50, required=False)
    account_type = serializers.CharField(max_length=50, required=False)
    account_number = serializers.CharField(max_length=50, required=False)
    account_holder_name = serializers.CharField(max_length=200, required=False)
    bic_swift = serializers.CharField(max_length=50, required=False)
    iban = serializers.CharField(max_length=50, required=False)
    bsb_code = serializers.CharField(max_length=50, required=False)
    bank_name = serializers.CharField(max_length=50, required=False)
    ifsc_code = serializers.CharField(max_length=50, required=False)
    branch_code = serializers.CharField(max_length=50, required=False)
    routing_number = serializers.CharField(max_length=50, required=False)
    clearing_number = serializers.CharField(max_length=50, required=False)
    institution_number = serializers.CharField(max_length=50, required=False)
    sort_code = serializers.CharField(max_length=50, required=False)
    bank_code = serializers.CharField(max_length=50, required=False)
    card_number = serializers.CharField(max_length=50, required=False)
    interac_account = serializers.CharField(max_length=50, required=False)
    aba_routing_number = serializers.CharField(max_length=50, required=False)
    bank_country = serializers.CharField(max_length=50, required=False)
