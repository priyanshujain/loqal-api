from django.conf import settings
from django.utils.translation import gettext as _

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.account.dbapi import (get_consumer_account_by_phone_number,
                                get_consumer_account_by_username)
from apps.payment.dbapi import get_payment_qrcode
from apps.payment.options import DisputeReasonType


class PaymentValidatorBase(serializers.ValidationSerializer):
    amount = serializers.DecimalField(
        min_value=1,
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        coerce_to_string=False,
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        amount = attrs.get("amount")
        tip_amount = attrs.get("tip_amount")

        if amount < 1.00:
            raise ValidationError(
                {
                    "amount": [
                        ErrorDetail(
                            _("Amount should be greater than a dollar.")
                        )
                    ]
                }
            )
        return attrs


class CreateMerchantPaymentValidator(PaymentValidatorBase):
    merchant_id = serializers.UUIDField()
    qrcode_id = serializers.CharField(required=False, allow_blank=True)
    tip_amount = serializers.DecimalField(
        min_value=0,
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        coerce_to_string=False,
    )


class CreatePaymentRequestValidator(PaymentValidatorBase):
    requested_to_loqal_id = serializers.CharField(required=False)
    requested_to_phone_number = serializers.CharField(required=False)
    is_phone_number_based = serializers.BooleanField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        is_phone_number_based = attrs.get("is_phone_number_based")
        loqal_id = attrs.get("requested_to_loqal_id")
        phone_number = attrs.get("requested_to_phone_number")

        if is_phone_number_based:
            if not phone_number:
                raise ValidationError(
                    {
                        "phone_number": [
                            ErrorDetail(
                                _(
                                    "Phone number can not be empty if you want to create phone number based payment request."
                                )
                            )
                        ]
                    }
                )
            consumer_account = get_consumer_account_by_phone_number(
                phone_number=phone_number
            )
            if not consumer_account:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("No user exists with given phone number.")
                        )
                    }
                )
        else:
            if not loqal_id:
                raise ValidationError(
                    {
                        "requested_to_loqal_id": [
                            ErrorDetail(
                                _(
                                    "Loqal ID can not be empty if you want to create Loqal ID based payment request."
                                )
                            )
                        ]
                    }
                )
            consumer_account = get_consumer_account_by_username(
                username=loqal_id
            )
            if not consumer_account:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("No user exists with given Loqal ID.")
                        )
                    }
                )
        return attrs


class AssignPaymentQrCodeValidator(serializers.ValidationSerializer):
    qrcode_id = serializers.CharField(max_length=6)
    cashier_id = serializers.IntegerField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        qrcode_id = attrs.get("qrcode_id")
        qrcode = get_payment_qrcode(qrcode_id=qrcode_id)
        if not qrcode:
            raise ValidationError(
                {
                    "qrcode_id": [
                        ErrorDetail(_("Provided QR Code is not valid."))
                    ]
                }
            )
        
        if qrcode.cashier:
            raise ValidationError(
                {
                    "detail": [
                        ErrorDetail(_("Provided QR Code is already being used by another merchant."))
                    ]
                }
            )
        return attrs


class ApprovePaymentRequestValidator(serializers.ValidationSerializer):
    payment_request_id = serializers.IntegerField()
    tip_amount = serializers.DecimalField(
        min_value=0,
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        coerce_to_string=False,
    )


class RejectPaymentRequestValidator(serializers.ValidationSerializer):
    payment_request_id = serializers.IntegerField()


class CreateRefundValidator(serializers.ValidationSerializer):
    payment_id = serializers.CharField()
    amount = serializers.DecimalField(
        min_value=1,
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        coerce_to_string=False,
    )


class CreateDisputeValidator(serializers.ValidationSerializer):
    transaction_tracking_id = serializers.CharField()
    reason_message = serializers.CharField(max_length=2 * 1024)
    reason_type = serializers.ChoiceField(choices=DisputeReasonType.choices)
