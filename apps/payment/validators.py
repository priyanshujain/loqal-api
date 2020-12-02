from django.utils.translation import gettext as _

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.account.options import AccountSupportedCurrencies


class CreatePaymentRequestSerializer(serializers.ValidationSerializer):
    beneficiary_id = serializers.IntegerField()
    target_amount = serializers.FloatField(min_value=0)
    source_currency = serializers.ChoiceField(
        choices=AccountSupportedCurrencies.choices()
    )
    ref_document = serializers.JSONField(default={})
    payment_reference = serializers.CharField(
        max_length=255, required=False, default=""
    )
    purpose_of_payment = serializers.CharField(max_length=255)
    purpose_of_payment_code = serializers.CharField(max_length=255)
    approver_ids = serializers.ListField(
        child=serializers.IntegerField(), default=[]
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        target_amount = attrs.get("target_amount")

        if target_amount <= 0:
            raise ValidationError(
                {
                    "target_amount": [
                        ErrorDetail(_("Amount should be greater than zero."))
                    ]
                }
            )
        return attrs
