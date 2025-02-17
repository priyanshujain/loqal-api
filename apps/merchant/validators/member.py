from api import serializers
from apps.account.validators import MerchantAccountSignupValidatorBase
from apps.merchant.options import AllowedFeatureAcessTypes, FeatureAcessTypes

__all__ = (
    "MemberInviteValidator",
    "UpdateMemberInviteValidator",
    "MemberSignupValidator",
    "UpdateMemberRoleValidator",
    "DisableMemberValidator",
    "EditMemberProfileValidator",
    "CreateFeatureAccessRoleValidator",
    "UpdateFeatureAccessRoleValidator",
    "DeleteFeatureAccessRoleValidator",
)


class FeatureAccessRoleValidatorBase(serializers.ValidationSerializer):
    is_full_access = serializers.BooleanField()
    payment_requests = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.PAYMENT_REQUESTS
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    payment_history = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.PAYMENT_HISTORY
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    settlements = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.SETTLEMENTS
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    refunds = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.REFUNDS
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    disputes = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.DISPUTES
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    customers = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.CUSTOMERS
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    bank_accounts = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.BANK_ACCOUNTS
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    qr_codes = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.QR_CODES
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    store_profile = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.STORE_PROFILE
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    team_management = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.TEAM_MANAGEMENT
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    loyalty_program = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.LOYALTY_PROGRAM
        ),
        allow_empty=True,
        required=False,
        default=[],
    )
    merchant_settings = serializers.ListField(
        child=serializers.EnumCharChoiceField(
            choices=AllowedFeatureAcessTypes.MERCHANT_SETTINGS
        ),
        allow_empty=True,
        required=False,
        default=[],
    )


class MemberInviteValidator(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=1024)
    last_name = serializers.CharField(
        max_length=1024, default="", required=False
    )
    email = serializers.EmailField(max_length=255)
    position = serializers.CharField(max_length=256)
    role = FeatureAccessRoleValidatorBase()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["email"] = str(attrs["email"]).lower()
        return attrs


class UpdateMemberInviteValidator(serializers.ValidationSerializer):
    invite_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=1024)
    last_name = serializers.CharField(
        max_length=1024, default="", required=False
    )
    email = serializers.EmailField(max_length=255)
    position = serializers.CharField(max_length=256)
    role = FeatureAccessRoleValidatorBase()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["email"] = str(attrs["email"]).lower()
        return attrs


class MemberSignupValidator(MerchantAccountSignupValidatorBase):
    token = serializers.CharField(max_length=256)
    position = serializers.CharField(max_length=256)


class UpdateMemberRoleValidator(serializers.ValidationSerializer):
    member_id = serializers.IntegerField()
    role = FeatureAccessRoleValidatorBase()


class DisableMemberValidator(serializers.ValidationSerializer):
    member_id = serializers.IntegerField()


class EditMemberProfileValidator(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)
    position = serializers.CharField(max_length=64)
    phone_number = serializers.CharField(max_length=10)


class CreateFeatureAccessRoleValidator(FeatureAccessRoleValidatorBase):
    role_name = serializers.CharField(max_length=256)


class UpdateFeatureAccessRoleValidator(FeatureAccessRoleValidatorBase):
    role_id = serializers.IntegerField()


class DeleteFeatureAccessRoleValidator(serializers.ValidationSerializer):
    role_id = serializers.IntegerField()
