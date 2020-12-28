from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext as _

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.merchant.shortcuts import validate_category
from apps.user.dbapi import get_user_by_phone
from lib.auth import password_validation

__all__ = ("CreateMerchantAccountValidator",)


class CreateMerchantAccountValidator(serializers.ValidationSerializer):
    company_name = serializers.CharField(max_length=500)
    address = serializers.AddressSerializer()
    category = serializers.CharField(max_length=32)
    sub_category = serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=512)
    last_name = serializers.CharField(max_length=512)
    email = serializers.EmailField(max_length=254)
    phone_number = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=64)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        category = attrs.get("category")
        sub_category = attrs.get("sub_category")
        password = attrs.get("password")

        if not validate_category(category=category, sub_category=sub_category):
            raise ValidationError(
                {"category": ErrorDetail(_("Provided category is not valid."))}
            )

        phone_number = attrs.get("phone_number")
        if len(phone_number) != 10:
            raise ValidationError(
                {
                    "phone_number": ErrorDetail(
                        _("Phone number should be consisting of 10 digits.")
                    )
                }
            )

        user = get_user_by_phone(phone_number=phone_number)
        if user:
            raise ValidationError(
                {
                    "phone_number": ErrorDetail(
                        _("A user already exist with this phone number.")
                    )
                }
            )
        try:
            password_validation.validate_password(password)
        except DjangoValidationError as error:
            raise ValidationError({"password": error.messages})
        return attrs
