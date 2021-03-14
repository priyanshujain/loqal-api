from decimal import Decimal

from api.services import ServiceBase
from apps.reward.dbapi import get_debit_reward_usage
from apps.reward.options import RewardValueType

__all__ = ("CheckReturnAmount",)


class CheckReturnRewardCreditAmount(ServiceBase):
    def __init__(self, order, amount):
        self.order = order
        self.amount = amount

    def handle(self):
        order = self.order
        reward_usage = None
        return_reward_value = Decimal(0.0)
        updated_reward_value = Decimal(0.0)
        reclaim_reward_value = Decimal(0.0)

        reward_usage = get_debit_reward_usage(order_id=order.id)
        if not reward_usage:
            return None
        if reward_usage.reward_value_type == RewardValueType.FIXED_AMOUNT:
            if reward_usage.total_amount < self.amount:
                return_reward_value = reward_usage.total_amount
            else:
                return_reward_value = self.amount
                updated_reward_value = (
                    reward_usage.total_amount - return_reward_value
                )
        else:
            reward_usage_item = None

            try:
                reward_usage_item = reward_usage.items.first()
                voucher_reward = reward_usage_item.voucher_reward
                remaing_sale_amount = (
                    order.total_amount
                    - order.total_return_amount
                    - self.amount
                )
                updated_reward_value = (
                    remaing_sale_amount * voucher_reward.value / 100
                )
                reclaim_reward_value = (
                    reward_usage.total_amount - updated_reward_value
                )
            except Exception:
                pass

        return {
            "return_reward_value": return_reward_value,
            "updated_reward_value": updated_reward_value,
            "reclaim_reward_value": reclaim_reward_value,
            "reward_usage": reward_usage,
        }
