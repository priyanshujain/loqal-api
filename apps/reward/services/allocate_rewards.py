from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from api.services import ServiceBase
from apps.order.dbapi import get_orders_in_period
from apps.reward.dbapi import (create_cash_reward, create_new_cash_usage,
                               create_new_voucher_usage,
                               create_reward_credit_event,
                               create_voucher_reward,
                               get_current_loyalty_program)
from apps.reward.options import LoyaltyParameters, RewardValueType

__all__ = ("AllocateRewards",)


class AllocateRewards(ServiceBase):
    def __init__(self, payment):
        self.payment = payment

    def handle(self):
        payment = self.payment
        order = payment.order
        merchant = order.merchant
        consumer = order.consumer
        loyalty_program = get_current_loyalty_program(merchant_id=merchant.id)
        if not loyalty_program:
            return None

        program_start_date = loyalty_program.program_start_date
        program_end_date = loyalty_program.program_end_date
        if not program_end_date:
            program_end_date = timezone.now()

        orders = get_orders_in_period(
            consumer_id=consumer.id,
            merchant_id=merchant.id,
            start_date=program_start_date,
            end_date=program_end_date,
        )

        if loyalty_program.loyalty_parameter == LoyaltyParameters.AMOUNT_SPENT:
            order_spent = orders.aggregate(
                total_net_amount=Sum("total_net_amount"),
                total_return_amount=Sum("total_return_amount"),
            )
            total_net_spent = (
                order_spent["total_net_amount"]
                - order_spent["total_return_amount"]
            )
            if total_net_spent >= loyalty_program.min_total_purchase:
                # Create reward
                reward_message = self._create_reward(
                    loyalty_program=loyalty_program,
                    consumer=consumer,
                    orders=orders,
                )
                return {
                    "reward_message": reward_message,
                    "loyalty_messge": (
                        "You have spent "
                        f"${loyalty_program.min_total_purchase} at "
                        f"{loyalty_program.merchant.profile.full_name}."
                    ),
                }
        else:
            order_count = (
                orders.aggregate(
                    count=Count("id"),
                ).get("count")
                or 0
            )

            if order_count >= loyalty_program.min_visits:
                reward_message = self._create_reward(
                    loyalty_program=loyalty_program,
                    consumer=consumer,
                    orders=orders,
                )
                return {
                    "reward_message": reward_message,
                    "loyalty_messge": (
                        "You have made "
                        f"{loyalty_program.min_visits} purchases at "
                        f"{loyalty_program.merchant.profile.full_name}."
                    ),
                }

        return None

    def _create_reward(self, loyalty_program, consumer, orders):
        if loyalty_program.reward_value_type == RewardValueType.FIXED_AMOUNT:
            cash_reward = create_cash_reward(
                value=loyalty_program.reward_value,
                loyalty_program_id=loyalty_program.id,
                consumer_id=consumer.id,
            )
            create_reward_credit_event(
                merchant_id=loyalty_program.merchant.id,
                consumer_id=consumer.id,
                reward_value_type=RewardValueType.FIXED_AMOUNT,
                value=cash_reward.available_value,
                cash_reward=cash_reward,
            )
            if cash_reward:
                orders.update(cash_reward=cash_reward, is_rewarded=True)
                create_new_cash_usage(cash_reward_id=cash_reward.id)
            return (
                f"You have received a cash reward of ${cash_reward.available_value}."
                " You can use it for your future purchases at "
                f"{loyalty_program.merchant.profile.full_name}"
            )
        else:
            voucher_reward = create_voucher_reward(
                value=loyalty_program.reward_value,
                max_value=loyalty_program.reward_value_maximum,
                loyalty_program_id=loyalty_program.id,
                consumer_id=consumer.id,
            )
            create_reward_credit_event(
                merchant_id=loyalty_program.merchant.id,
                consumer_id=consumer.id,
                reward_value_type=RewardValueType.FIXED_AMOUNT,
                value=voucher_reward.value,
                voucher_reward=voucher_reward,
            )
            if voucher_reward:
                orders.update(voucher_reward=voucher_reward, is_rewarded=True)
                create_new_voucher_usage(voucher_reward_id=voucher_reward.id)
            return (
                "You have received a reward consists of voucher "
                f"${voucher_reward.value}% off on the next "
                f"transaction(upto ${voucher_reward.reward_value_maximum})."
                " You can use it for your future purchases at "
                f"{loyalty_program.merchant.profile.full_name}"
            )
