from decimal import Decimal

from django.db.models import Sum

from api.services import ServiceBase
from apps.reward.dbapi import (get_cash_refund_usages, get_debit_reward_usage,
                               get_voucher_refund_usages)
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
            credit_usages = get_cash_refund_usages(order_id=order.id)
            credited_cash_total = credit_usages.aggregate(
                total=Sum("total_amount")
            ).get("total") or Decimal(0.0)
            remaining_cash_reward_applied = (
                reward_usage.total_amount - credited_cash_total
            )
            if remaining_cash_reward_applied < self.amount:
                return_reward_value = remaining_cash_reward_applied
            else:
                return_reward_value = self.amount
                updated_reward_value = (
                    remaining_cash_reward_applied - return_reward_value
                )
        else:
            reward_usage_item = None
            try:
                reward_usage_item = reward_usage.items.first()
                voucher_reward = reward_usage_item.voucher_reward
                return_voucher_usages = get_voucher_refund_usages(
                    order_id=order.id
                )
                reclaimed_voucher_amount = return_voucher_usages.aggregate(
                    total=Sum("total_amount")
                ).get("total") or Decimal(0.0)
                remaing_sale_amount = (
                    order.total_amount
                    - order.total_return_amount
                    - order.total_reclaimed_amount
                    - self.amount
                )
                updated_reward_value = (
                    remaing_sale_amount * voucher_reward.value / 100
                )
                if updated_reward_value > voucher_reward.value_maximum:
                    updated_reward_value = voucher_reward.value_maximum

                existing_voucher_reward_amount = (
                    reward_usage.total_amount - reclaimed_voucher_amount
                )
                if updated_reward_value < existing_voucher_reward_amount:
                    reclaim_reward_value = (
                        existing_voucher_reward_amount - updated_reward_value
                    )

            except Exception:
                pass

        return {
            "return_reward_value": return_reward_value,
            "updated_reward_value": updated_reward_value,
            "reclaim_reward_value": reclaim_reward_value,
            "reward_usage": reward_usage,
        }
