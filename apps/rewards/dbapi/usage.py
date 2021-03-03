from apps.rewards.models import RewardUsage, RewardUsageItem
from django.db.utils import IntegrityError


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


def create_debit_reward_usage_item(amount, usage_id, voucher_reward=None, cash_reward=None):
    try:
        return RewardUsageItem.objects.create(
            amount=amount,
            usage_id=usage_id,
            voucher_reward=voucher_reward,
            cash_reward=cash_reward,
        )
    except IntegrityError:
        return None


