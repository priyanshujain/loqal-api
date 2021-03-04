from decimal import Decimal

from django.utils.translation import gettext as _

from api.services import ServiceBase
from apps.order.dbapi import create_base_order
from apps.order.options import OrderType
from apps.rewards.dbapi import (create_debit_reward_usage,
                                create_debit_reward_usage_item,
                                create_reward_debit_event)
from apps.rewards.options import RewardValueType

from .check_reward_available import CheckRewardAvailable

__all__ = ("CreateOrder",)


class CreateOrder(ServiceBase):
    def __init__(
        self, consumer_id, merchant_id, amount, order_type=OrderType.ONLINE
    ):
        self.consumer_id = consumer_id
        self.merchant_id = merchant_id
        self.amount = amount
        self.order_type = order_type

    def handle(self):
        reward = CheckRewardAvailable(
            consumer_id=self.consumer_id, merchant_id=self.merchant_id
        ).handle()
        if not reward:
            return self._factory_order()

        if reward["type"] == RewardValueType.FIXED_AMOUNT:
            redeemable_reward_amount = Decimal(0.0)
            cash_rewards = reward["object"]
            total_available = reward["total_available"]
            if self.amount >= total_available:
                redeemable_reward_amount = total_available
            else:
                redeemable_reward_amount = self.amount
            return self._factory_cash_reward_order(
                redeemable_reward_amount=redeemable_reward_amount,
                cash_rewards=cash_rewards,
            )
        else:
            redeemable_reward_amount = Decimal(0.0)
            voucher = reward["object"]
            percentage_amount = (self.amount * voucher.value) / 100
            if percentage_amount > voucher.value_maximum:
                redeemable_reward_amount = voucher.value_maximum
            else:
                redeemable_reward_amount = percentage_amount
            return self._factory_voucher_reward_order(
                redeemable_reward_amount=redeemable_reward_amount,
                voucher=voucher,
            )

    def _factory_cash_reward_order(
        self, redeemable_reward_amount, cash_rewards
    ):
        order = self._factory_order()
        reward_usage = create_debit_reward_usage(
            total_amount=redeemable_reward_amount,
            reward_value_type=RewardValueType.FIXED_AMOUNT,
            order_id=order.id,
        )
        order.update_discount(
            amount=redeemable_reward_amount,
            name=f"Loyalty reward cash credits applied.",
        )
        redeemed_amount = 0
        for cash_reward in cash_rewards:
            total_cash_available = cash_reward.available_value
            redeemed_item_amount = 0
            if (
                redeemed_amount + total_cash_available
            ) > redeemable_reward_amount:
                redeemed_item_amount = (
                    redeemable_reward_amount - redeemed_amount
                )
            else:
                redeemed_item_amount = total_cash_available
            usage_item = create_debit_reward_usage_item(
                amount=redeemed_item_amount,
                usage_id=reward_usage.id,
                cash_reward=cash_reward,
            )
            create_reward_debit_event(
                merchant_id=self.merchant_id,
                consumer_id=self.consumer_id,
                reward_value_type=RewardValueType.FIXED_AMOUNT,
                value=redeemed_item_amount,
                reward_usage_item=usage_item,
                cash_reward=cash_reward,
            )
            redeemed_amount += usage_item.amount
            cash_reward.update_usage(used_amount=usage_item.amount)
            if redeemable_reward_amount != total_cash_available:
                break
        return order

    def _factory_voucher_reward_order(self, redeemable_reward_amount, voucher):
        order = self._factory_order()
        reward_usage = create_debit_reward_usage(
            total_amount=redeemable_reward_amount,
            reward_value_type=RewardValueType.PERCENTAGE,
            order_id=order.id,
        )
        order.update_discount(
            amount=redeemable_reward_amount,
            name=f"Loyalty reward voucher applied.",
        )
        usage_item = create_debit_reward_usage_item(
            amount=redeemable_reward_amount,
            usage_id=reward_usage.id,
            voucher_reward=voucher,
        )
        create_reward_debit_event(
            merchant_id=self.merchant_id,
            consumer_id=self.consumer_id,
            reward_value_type=RewardValueType.FIXED_AMOUNT,
            value=redeemable_reward_amount,
            reward_usage_item=usage_item,
            voucher_reward=voucher,
        )
        voucher.update_usage()
        return order

    def _factory_order(self):
        return create_base_order(
            merchant_id=self.merchant_id,
            consumer_id=self.consumer_id,
            amount=self.amount,
            order_type=self.order_type,
        )
