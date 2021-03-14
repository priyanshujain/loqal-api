from decimal import Decimal

from api.services import ServiceBase
from apps.reward.dbapi import (create_cash_refund_usage,
                               create_cash_refund_usage_item,
                               create_reward_credit_event,
                               create_reward_reclaimed_event,
                               create_voucher_refund)
from apps.reward.options import RewardValueType

__all__ = ("ReturnRewards",)


class ReturnRewards(ServiceBase):
    def __init__(
        self,
        return_reward_value,
        updated_reward_value,
        reclaim_reward_value,
        reward_usage,
    ):
        self.return_reward_value = return_reward_value
        self.updated_reward_value = updated_reward_value
        self.reclaim_reward_value = reclaim_reward_value
        self.reward_usage = reward_usage

    def handle(self):
        reward_usage = self.reward_usage
        reward_value_type = reward_usage.reward_value_type
        if reward_value_type == RewardValueType.PERCENTAGE:
            try:
                reward_usage_item = reward_usage.items.first()
                voucher_reward = reward_usage_item.voucher_reward
                if self.updated_reward_value == Decimal(0.0):
                    (
                        credit_reward_usage,
                        credit_reward_usage_item,
                    ) = create_voucher_refund(
                        order_id=reward_usage.order.id,
                        voucher_reward_id=voucher_reward.id,
                    )
                    voucher_reward.refund()
                    create_reward_credit_event(
                        merchant_id=reward_usage.order.merchant.id,
                        consumer_id=reward_usage.order.consumer.id,
                        reward_value_type=reward_usage.reward_value_type,
                        value=None,
                        cash_reward=None,
                        voucher_reward=voucher_reward,
                        reward_usage_item=credit_reward_usage_item,
                    )
                    return credit_reward_usage
                else:
                    (
                        credit_reward_usage,
                        credit_reward_usage_item,
                    ) = create_voucher_refund(
                        order_id=reward_usage.order.id,
                        voucher_reward_id=voucher_reward.id,
                        amount=self.reclaim_reward_value,
                    )
                    create_reward_reclaimed_event(
                        merchant_id=reward_usage.order.merchant.id,
                        consumer_id=reward_usage.order.consumer.id,
                        reward_value_type=reward_usage.reward_value_type,
                        value=self.reclaim_reward_value,
                        cash_reward=None,
                        voucher_reward=voucher_reward,
                        reward_usage_item=credit_reward_usage_item,
                    )
                    return credit_reward_usage
            except Exception:
                return None
        else:
            try:
                reward_usage_items = reward_usage.items.order_by("created_at")
                refunded_amount = Decimal(0.0)
                credit_reward_usage = create_cash_refund_usage(
                    order_id=reward_usage.order.id,
                    amount=self.return_reward_value,
                )
                for reward_usage_item in reward_usage_items:
                    refunded_amount_item = Decimal(0.0)
                    cash_reward = reward_usage_item.cash_reward
                    if (
                        refunded_amount + reward_usage_item.amount
                    ) < self.return_reward_value:
                        refunded_amount_item = reward_usage_item.amount
                    else:
                        refunded_amount_item = (
                            self.return_reward_value - refunded_amount
                        )
                    credit_reward_usage_item = create_cash_refund_usage_item(
                        usage_id=credit_reward_usage.id,
                        cash_reward_id=cash_reward.id,
                        amount=refunded_amount_item,
                    )
                    cash_reward.refund(refunded_amount_item)
                    create_reward_credit_event(
                        merchant_id=reward_usage.order.merchant.id,
                        consumer_id=reward_usage.order.consumer.id,
                        reward_value_type=reward_usage.reward_value_type,
                        value=refunded_amount_item,
                        cash_reward=cash_reward,
                        voucher_reward=None,
                        reward_usage_item=credit_reward_usage_item,
                    )
                    refunded_amount += refunded_amount_item
                    if refunded_amount == self.return_reward_value:
                        break
                return credit_reward_usage
            except Exception:
                return None
