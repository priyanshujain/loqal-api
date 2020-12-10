from api import serializers
from apps.merchant.options import FeatureAcessTypes

__all__ = (
    "MemberInviteValidator",
    "UpdateMemberInviteValidator",
    "MemberSignupValidator",
    "UpdateMemberRoleValidator",
    "DisableMemberValidator",
    "CreateFeatureAccessRoleValidator",
    "UpdateFeatureAccessRoleValidator",
    "DeleteFeatureAccessRoleValidator",
)


class MemberInviteValidator(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=1024)
    last_name = serializers.CharField(
        max_length=1024, default="", required=False
    )
    email = serializers.EmailField(max_length=255)
    position = serializers.CharField(max_length=256)
    role_id = serializers.IntegerField()


class UpdateMemberInviteValidator(serializers.ValidationSerializer):
    invite_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=1024)
    last_name = serializers.CharField(
        max_length=1024, default="", required=False
    )
    email = serializers.EmailField(max_length=255)
    position = serializers.CharField(max_length=256)
    role_id = serializers.IntegerField()


class MemberSignupValidator(serializers.ValidationSerializer):
    invite_key = serializers.CharField(max_length=256)
    first_name = serializers.CharField(max_length=1024)
    last_name = serializers.CharField(
        max_length=1024, default="", required=False
    )
    phone_number = serializers.CharField(
        max_length=20, default="", required=False
    )
    position = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=128)


class UpdateMemberRoleValidator(serializers.ValidationSerializer):
    member_id = serializers.IntegerField()
    role_id = serializers.IntegerField()


class DisableMemberValidator(serializers.ValidationSerializer):
    member_id = serializers.IntegerField()


class FeatureAccessRoleValidatorBase(serializers.ValidationSerializer):
    description = serializers.CharField(
        max_length=1024, default="", required=False
    )
    team_and_roles = serializers.ListField(
        child=serializers.ChoiceField(choices=FeatureAcessTypes.choices),
        allow_empty=True,
        required=False,
        default={},
    )
    beneficiaries = serializers.ListField(
        child=serializers.ChoiceField(choices=FeatureAcessTypes.choices),
        allow_empty=True,
        required=False,
        default={},
    )
    transactions = serializers.ListField(
        child=serializers.ChoiceField(choices=FeatureAcessTypes.choices),
        allow_empty=True,
        required=False,
        default={},
    )
    direct_debit_accounts = serializers.ListField(
        child=serializers.ChoiceField(choices=FeatureAcessTypes.choices),
        allow_empty=True,
        required=False,
        default={},
    )
    settings = serializers.ListField(
        child=serializers.ChoiceField(choices=FeatureAcessTypes.choices),
        allow_empty=True,
        required=False,
        default={},
    )


class CreateFeatureAccessRoleValidator(FeatureAccessRoleValidatorBase):
    role_name = serializers.CharField(max_length=256)


class UpdateFeatureAccessRoleValidator(FeatureAccessRoleValidatorBase):
    role_id = serializers.IntegerField()


class DeleteFeatureAccessRoleValidator(serializers.ValidationSerializer):
    role_id = serializers.IntegerField()
