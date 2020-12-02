from api import serializers
from apps.approval.models import ApprovalRequest
from apps.beneficiary.responses import BeneficiaryResponse
from apps.member.models import AccountMember

from .models import PaymentRequest, RateQuote, Transaction


class PaymentRequestModelResponse(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = "__all__"


class QuoteModelResponse(serializers.ModelSerializer):
    class Meta:
        model = RateQuote
        fields = "__all__"


class TransactionResponse(serializers.ModelSerializer):
    quote = QuoteModelResponse(read_only=True)
    beneficiary = BeneficiaryResponse(
        source="payment_request.beneficiary", read_only=True
    )
    payment_request = PaymentRequestModelResponse(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"


class ApprovalRequestResponse(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = "__all__"


class PaymentRequestResponse(serializers.ModelSerializer):
    beneficiary = BeneficiaryResponse(read_only=True)
    approval_requests = ApprovalRequestResponse(
        source="approvalrequest_set", many=True, read_only=True
    )

    class Meta:
        model = PaymentRequest
        fields = "__all__"


class TempModelSerializer(serializers.ModelSerializer):
    @property
    def response(self):
        return self.data


class ApproversResponse(TempModelSerializer):
    first_name = serializers.CharField(
        source="profile.first_name", read_only=True
    )
    last_name = serializers.CharField(
        source="profile.last_name", read_only=True
    )
    role_name = serializers.CharField(source="role.role_name", read_only=True)
    email = serializers.CharField(source="profile.user.email", read_only=True)

    class Meta:
        model = AccountMember
        fields = (
            "id",
            "position",
            "first_name",
            "last_name",
            "role_name",
            "email",
        )
