import decimal

from django.utils.translation import gettext as _

from api import serializers
from api.exceptions import ErrorDetail, ValidationError


class CreatePaymentValidator(serializers.ValidationSerializer):
    merchant_id = serializers.UUIDField()
    payment_amount = serializers.FloatField(min_value=0)
    tip_amount = serializers.FloatField(min_value=0)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        payment_amount = attrs.get("payment_amount")
        tip_amount = attrs.get("tip_amount")

        if payment_amount < 1.00:
            raise ValidationError(
                {"amount": [ErrorDetail(_("Amount should be greater than a dollar."))]}
            )
        payment_amount_decimal = decimal.Decimal(str(payment_amount))
        if payment_amount_decimal.as_tuple().exponent > 2:
            raise ValidationError(
                {
                    "payment_amount": [
                        ErrorDetail(_("Amount can only have two digits after decimal."))
                    ]
                }
            )
        tip_amount_decimal = decimal.Decimal(str(tip_amount))
        if tip_amount_decimal.as_tuple().exponent > 2:
            raise ValidationError(
                {
                    "tip_amount": [
                        ErrorDetail(
                            _("Tip amount can only have two digits after decimal.")
                        )
                    ]
                }
            )
        return attrs


class AssignPaymentQrCodeValidator(serializers.ValidationSerializer):
    qrcode_id = serializers.CharField(max_length=6)
    cashier_id = serializers.IntegerField()

    def validate(self, attr):
        return attr
