from enum import Flag
from django.db.utils import IntegrityError

from apps.rewards.models import (CashReward, LoyaltyProgram, RewardUsage,
                                 RewardUsageItem, VoucherReward)


def create_cash_reward(value, loyalty_program_id, consumer_id):
    try:
        return CashReward.objects.create(
            available_value=value,
            loyalty_program_id=loyalty_program_id,
            consumer_id=consumer_id,
        )
    except IntegrityError:
        return None


def create_voucher_reward(value, max_value, loyalty_program_id, consumer_id):
    try:
        return VoucherReward.objects.create(
            value=value,
            value_maximum=max_value,
            loyalty_program_id=loyalty_program_id,
            consumer_id=consumer_id,
        )
    except IntegrityError:
        return None


def get_cash_rewards(merchant_id, consumer_id):
    return CashReward.objects.filter(
        loyalty_program__merchant_id=merchant_id,
        consumer_id=consumer_id,
        available_value__gt=0,
    ).order_by("created_at")


def get_voucher_rewards(merchant_id, consumer_id):
    return VoucherReward.objects.filter(
        loyalty_program__merchant_id=merchant_id,
        consumer_id=consumer_id,
        is_used=False,
    ).order_by("created_at")
