from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.views import ConsumerAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.merchant.responses import MerchantBasicDetailsResponse
from apps.order.dbapi import get_orders_in_period, get_rewarded_merchant_orders
from apps.order.services import CheckRewardAvailable
from apps.reward.dbapi import (get_all_reward_usage, get_cash_rewards,
                               get_current_loyalty_program,
                               get_voucher_rewards)
from apps.reward.options import RewardValueType
from apps.reward.responses import (CashRewardResponse, LoyaltyProgramResponse,
                                   RewardUsageItemResponse,
                                   VoucherRewardResponse)


class CheckRewardsAvailableAPI(ConsumerAPIView):
    def get(self, request, merchant_id):
        merchant = get_merchant_account_by_uid(merchant_uid=merchant_id)
        if not merchant:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Given merchant is not valid. Please check back and try again."
                        )
                    )
                }
            )
        reward_data = CheckRewardAvailable(
            consumer_id=request.consumer_account.id,
            merchant_id=merchant.id,
        ).handle()
        if not reward_data:
            return self.response()
        elif reward_data["type"] == RewardValueType.FIXED_AMOUNT:
            return self.response(
                {
                    "type": {
                        "value": RewardValueType.FIXED_AMOUNT.value,
                        "label": RewardValueType.FIXED_AMOUNT.label,
                    },
                    "value": reward_data["total_available"],
                }
            )
        else:
            return self.response(
                {
                    "type": {
                        "value": RewardValueType.PERCENTAGE.value,
                        "label": RewardValueType.PERCENTAGE.label,
                    },
                    "value_maximum": reward_data["value_maximum"],
                    "value": reward_data["value"],
                }
            )


class RewardedMerchantsAPI(ConsumerAPIView):
    def get(self, request):
        consumer = request.consumer_account
        rewarded_orders = get_rewarded_merchant_orders(consumer_id=consumer.id)
        merchants = []
        for order in rewarded_orders:
            merchant = MerchantBasicDetailsResponse(order.merchant).data
            merchant["store_visits"] = order.merchant.orders.count()
            cash_rewards = get_cash_rewards(
                merchant_id=order.merchant.id, consumer_id=order.consumer.id
            )
            merchant["cash_rewards"] = (
                cash_rewards.aggregate(total=Sum("available_value")).get(
                    "total"
                )
                or "0.0"
            )
            merchant["vouchers"] = get_voucher_rewards(
                merchant_id=order.merchant.id, consumer_id=order.consumer.id
            ).count()
            merchants.append(merchant)
        return self.response(merchants)


class MerchantRewardDetailsAPI(ConsumerAPIView):
    def get(self, request, merchant_id):
        merchant = get_merchant_account_by_uid(merchant_uid=merchant_id)
        if not merchant:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Given merchant is not valid. Please check back and try again."
                        )
                    )
                }
            )
        consumer = request.consumer_account
        reward_details = {}
        loyalty_program = get_current_loyalty_program(merchant_id=merchant.id)
        if not loyalty_program:
            reward_details["loyalty_program"] = {}
        else:
            reward_details["loyalty_program"] = LoyaltyProgramResponse(
                loyalty_program
            ).data
        cash_rewards = get_cash_rewards(
            merchant_id=merchant.id, consumer_id=consumer.id
        )
        reward_details["cash_rewards"] = CashRewardResponse(
            cash_rewards, many=True
        ).data
        voucher_rewards = get_voucher_rewards(
            merchant_id=merchant.id, consumer_id=consumer.id
        )
        reward_details["voucher_rewards"] = VoucherRewardResponse(
            voucher_rewards, many=True
        ).data

        if loyalty_program:
            orders = self._get_reward_orders(
                loyalty_program=loyalty_program,
                consumer=consumer,
                merchant=merchant,
            )
            reward_details["reward_in_process_orders"] = {
                "total_count": orders.count(),
                "total_sum": orders.aggregate(
                    total=Sum("total_net_amount")
                ).get("total")
                or "0.0",
            }

        reward_usage_items = get_all_reward_usage(
            merchant_id=merchant.id, consumer_id=consumer.id
        )
        reward_details["history"] = RewardUsageItemResponse(
            reward_usage_items, many=True
        ).data
        return self.response(reward_details)

    def _get_reward_orders(self, loyalty_program, consumer, merchant):
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
        return orders
