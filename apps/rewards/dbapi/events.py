from apps.rewards.models import RewardEvent
from apps.rewards.options import RewardEventType


def create_reward_credit_event(
    merchant_id,
    consumer_id,
    reward_value_type,
    value,
    cash_reward=None,
    voucher_reward=None,
    reward_usage_item=None,
):
    return RewardEvent.objects.create(
        merchant_id=merchant_id,
        consumer_id=consumer_id,
        event_type=RewardEventType.CREDITED,
        reward_value_type=reward_value_type,
        value=value,
        reward_usage_item=reward_usage_item,
        cash_reward=cash_reward,
        voucher_reward=voucher_reward,
    )


def create_reward_debit_event(
    merchant_id,
    consumer_id,
    reward_value_type,
    value,
    cash_reward=None,
    voucher_reward=None,
    reward_usage_item=None,
):
    return RewardEvent.objects.create(
        merchant_id=merchant_id,
        consumer_id=consumer_id,
        event_type=RewardEventType.DEBITED,
        reward_value_type=reward_value_type,
        value=value,
        reward_usage_item=reward_usage_item,
        cash_reward=cash_reward,
        voucher_reward=voucher_reward,
    )


def create_reward_reclaimed_event(
    merchant_id,
    consumer_id,
    reward_value_type,
    value,
    cash_reward=None,
    voucher_reward=None,
    reward_usage_item=None,
):
    return RewardEvent.objects.create(
        merchant_id=merchant_id,
        consumer_id=consumer_id,
        event_type=RewardEventType.RECLAIMED,
        reward_value_type=reward_value_type,
        value=value,
        reward_usage_item=reward_usage_item,
        cash_reward=cash_reward,
        voucher_reward=voucher_reward,
    )


def create_reward_refunded_event(
    merchant_id,
    consumer_id,
    reward_value_type,
    value,
    cash_reward=None,
    voucher_reward=None,
    reward_usage_item=None,
):
    return RewardEvent.objects.create(
        merchant_id=merchant_id,
        consumer_id=consumer_id,
        event_type=RewardEventType.REFUNDED,
        reward_value_type=reward_value_type,
        value=value,
        reward_usage_item=reward_usage_item,
        cash_reward=cash_reward,
        voucher_reward=voucher_reward,
    )


def create_reward_expired_event(
    merchant_id,
    consumer_id,
    reward_value_type,
    value,
    cash_reward=None,
    voucher_reward=None,
    reward_usage_item=None,
):
    return RewardEvent.objects.create(
        merchant_id=merchant_id,
        consumer_id=consumer_id,
        event_type=RewardEventType.EXPIRED,
        reward_value_type=reward_value_type,
        value=value,
        reward_usage_item=reward_usage_item,
        cash_reward=cash_reward,
        voucher_reward=voucher_reward,
    )
