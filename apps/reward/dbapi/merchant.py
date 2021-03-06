from django.db.utils import IntegrityError

from apps.reward.models import (CashReward, LoyaltyProgram, RewardUsage,
                                RewardUsageItem, VoucherReward)


def get_current_loyalty_program(merchant_id):
    try:
        return LoyaltyProgram.objects.get(
            merchant_id=merchant_id, is_active=True
        )
    except LoyaltyProgram.DoesNotExist:
        return None


def get_all_loyalty_program(merchant_id):
    try:
        return LoyaltyProgram.objects.filter(merchant_id=merchant_id)
    except LoyaltyProgram.DoesNotExist:
        return None


def create_loyalty_program(
    merchant_id,
    loyalty_parameter,
    program_start_date,
    program_end_date,
    reward_value_type,
    reward_value,
    min_total_purchase=0,
    min_visits=1,
    reward_value_maximum=0,
):
    try:
        return LoyaltyProgram.objects.create(
            merchant_id=merchant_id,
            loyalty_parameter=loyalty_parameter,
            program_start_date=program_start_date,
            program_end_date=program_end_date,
            reward_value_type=reward_value_type,
            reward_value=reward_value,
            min_total_purchase=min_total_purchase,
            min_visits=min_visits,
            reward_value_maximum=reward_value_maximum,
        )
    except IntegrityError:
        return None


def update_loyalty_program(
    merchant_id,
    loyalty_parameter,
    program_start_date,
    program_end_date,
    reward_value_type,
    reward_value,
    min_total_purchase=0,
    min_visits=1,
    reward_value_maximum=0,
):
    LoyaltyProgram.objects.filter(
        merchant_id=merchant_id, is_active=True
    ).update(
        loyalty_parameter=loyalty_parameter,
        program_start_date=program_start_date,
        program_end_date=program_end_date,
        reward_value_type=reward_value_type,
        reward_value=reward_value,
        min_total_purchase=min_total_purchase,
        min_visits=min_visits,
        reward_value_maximum=reward_value_maximum,
    )
