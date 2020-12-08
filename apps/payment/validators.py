from django.utils.translation import gettext as _
import decimal
from api import serializers
from api.exceptions import ErrorDetail, ValidationError


class CreatePaymentValidator(serializers.ValidationSerializer):
    merchant_id = serializers.IntegerField()
    amount = serializers.FloatField(min_value=0)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        amount = attrs.get("amount")

        if amount < 1.00:
            raise ValidationError(
                {
                    "amount": [
                        ErrorDetail(_("Amount should be greater than a dollar."))
                    ]
                }
            )
        amount_decimal = decimal.Decimal(str(amount))
        if amount_decimal.as_tuple().exponent > 2:
             raise ValidationError(
                {
                    "amount": [
                        ErrorDetail(_("Amount can only have two digits after decimal."))
                    ]
                }
            )
        return attrs
