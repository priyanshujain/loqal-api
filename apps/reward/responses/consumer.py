from decimal import Decimal

from api import serializers
from apps.payment.options import PaymentProcess
from apps.reward.models import (CashReward, LoyaltyProgram, RewardUsage,
                                RewardUsageItem, VoucherReward)


class CashRewardResponse(serializers.ModelSerializer):
    class Meta:
        model = CashReward
        fields = (
            "created_at",
            "available_value",
            "used_value",
            "is_full_used",
        )


class VoucherRewardResponse(serializers.ModelSerializer):
    class Meta:
        model = VoucherReward
        fields = (
            "created_at",
            "value",
            "value_maximum",
            "is_used",
        )


class RewardUsageItemResponse(serializers.ModelSerializer):
    cash_reward = CashRewardResponse(read_only=True)
    voucher_reward = VoucherRewardResponse(read_only=True)
    payment_tracking_id = serializers.CharField(
        source="usage.order.payment.payment_tracking_id", read_only=True
    )
    transaction_tracking_id = serializers.SerializerMethodField(
        "get_transaction_tracking_id"
    )
    order_id = serializers.CharField(source="usage.order.u_id", read_only=True)
    is_credit = serializers.BooleanField(
        source="usage.is_credit", read_only=True
    )

    class Meta:
        model = RewardUsageItem
        fields = (
            "created_at",
            "amount",
            "cash_reward",
            "voucher_reward",
            "is_credit",
            "is_reclaimed",
            "payment_tracking_id",
            "transaction_tracking_id",
            "order_id",
        )

    def get_transaction_tracking_id(self, obj):
        payment = None
        try:
            payment = obj.usage.order.payment
        except Exception:
            return None

        if not payment:
            return None

        transaction = None
        self.tip_amount = Decimal(0.0)
        if payment.payment_process == PaymentProcess.PAYMENT_REQUEST:
            payment_requests = payment.payment_requests
            if not payment_requests.exists():
                return None
            payment_request = payment_requests.first()
            transaction = payment_request.transaction
            self.tip_amount = payment_request.tip_amount

        if payment.payment_process in [
            PaymentProcess.QRCODE,
            PaymentProcess.DIRECT_APP,
        ]:
            direct_merchant_payments = payment.direct_merchant_payments
            if not direct_merchant_payments.exists():
                return None
            direct_merchant_payment = direct_merchant_payments.first()
            transaction = direct_merchant_payment.transaction
            self.tip_amount = direct_merchant_payment.tip_amount

        if transaction:
            return transaction.transaction_tracking_id
        return None
