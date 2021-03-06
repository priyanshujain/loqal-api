from django.db.utils import IntegrityError

from apps.reward.models import RewardUsage, RewardUsageItem
from apps.reward.options import RewardValueType


def create_debit_reward_usage(total_amount, reward_value_type, order_id):
    try:
        return RewardUsage.objects.create(
            total_amount=total_amount,
            is_credit=False,
            reward_value_type=reward_value_type,
            order_id=order_id,
        )
    except IntegrityError:
        return None


def create_debit_reward_usage_item(
    amount, usage_id, voucher_reward=None, cash_reward=None
):
    try:
        return RewardUsageItem.objects.create(
            amount=amount,
            usage_id=usage_id,
            voucher_reward=voucher_reward,
            cash_reward=cash_reward,
        )
    except IntegrityError:
        return None


def get_debit_reward_usage(order_id):
    try:
        return RewardUsage.objects.get(
            is_credit=False,
            order_id=order_id,
        )
    except RewardUsage.DoesNotExist:
        return None


def create_voucher_refund(order_id, voucher_reward_id, amount=None):
    try:
        reward_usage = RewardUsage.objects.create(
            is_credit=True,
            total_amount=amount,
            reward_value_type=RewardValueType.PERCENTAGE,
            order_id=order_id,
        )
        reward_usage_item = RewardUsageItem.objects.create(
            amount=amount,
            usage_id=reward_usage.id,
            voucher_reward_id=voucher_reward_id,
            is_reclaimed=True,
        )
        return reward_usage, reward_usage_item
    except IntegrityError:
        return None, None


def create_cash_refund_usage(order_id, amount):
    try:
        return RewardUsage.objects.create(
            is_credit=True,
            total_amount=amount,
            reward_value_type=RewardValueType.FIXED_AMOUNT,
            order_id=order_id,
        )
    except IntegrityError:
        return None


def create_cash_refund_usage_item(usage_id, cash_reward_id, amount):
    try:
        return RewardUsageItem.objects.create(
            usage_id=usage_id,
            amount=amount,
            cash_reward_id=cash_reward_id,
        )
    except IntegrityError:
        return None


def get_all_reward_usage(merchant_id, consumer_id):
    return RewardUsageItem.objects.filter(
        usage__order__merchant_id=merchant_id,
        usage__order__consumer_id=consumer_id,
    ).order_by("-created_at")
