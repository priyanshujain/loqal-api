from django.db.models import Q

from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.models import BeneficialOwner
from apps.merchant.options import BeneficialOwnerStatus

__all__ = (
    "MerchantAccountProfileResponse",
    "MerchantAccountStatusResponse",
)


class MerchantAccountProfileResponse(serializers.ModelSerializer):
    zip_code = serializers.CharField(source="account.zip_code", read_only=True)
    account_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_status", read_only=True
    )
    account_verification_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_verification_status", read_only=True
    )
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    merchant_id = serializers.CharField(source="u_id", read_only=True)
    beneficial_owner_verified = serializers.SerializerMethodField(
        "check_beneficial_owner_verified"
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "created_at",
            "zip_code",
            "company_email",
            "account_status",
            "account_verification_status",
            "merchant_id",
            "full_name",
            "beneficial_owner_verified",
        )

    def check_beneficial_owner_verified(self, obj):
        return (
            not BeneficialOwner.objects.filter(merchant_id=obj.id)
            .filter(~Q(status=BeneficialOwnerStatus.VERIFIED))
            .exists()
        )


class MerchantAccountStatusResponse(serializers.ModelSerializer):
    account_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_status", read_only=True
    )
    account_verification_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_verification_status", read_only=True
    )
    beneficial_owner_statuses = serializers.SerializerMethodField(
        "check_beneficial_owner_statuses"
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "account_status",
            "account_verification_status",
            "beneficial_owner_statuses",
        )

    def check_beneficial_owner_statuses(self, obj):
        statuses = []
        for beneficial_owner in BeneficialOwner.objects.filter(
            merchant_id=obj.id
        ):
            statuses.append(
                {
                    "id": beneficial_owner.id,
                    "status": {
                        "label": beneficial_owner.status.label,
                        "value": beneficial_owner.status.value,
                    },
                }
            )
        return statuses
