from django.db.models import Sum
from django.utils.translation import gettext as _

from api.services import ServiceBase
from apps.rewards.dbapi import get_cash_rewards, get_voucher_rewards
from apps.rewards.options import RewardValueType

__all__ = ("CheckRewardAvailable",)


class CheckRewardAvailable(ServiceBase):
    def __init__(self, consumer_id, merchant_id):
        self.consumer_id = consumer_id
        self.merchant_id = merchant_id

    def handle(self):
        cash_rewards = get_cash_rewards(
            consumer_id=self.consumer_id, merchant_id=self.merchant_id
        )
        if cash_rewards.exists():
            return self._cash_rewards_details(cash_rewards)
        else:
            voucher_rewards = get_voucher_rewards(
                consumer_id=self.consumer_id, merchant_id=self.merchant_id
            )
            if voucher_rewards.exists():
                return self._voucher_rewards_details(voucher_rewards)
            else:
                return None

    def _cash_rewards_details(self, cash_rewards):
        cash_reward = cash_rewards.aggregate(
            total_available=Sum("available_value")
        )
        cash_reward["type"] = RewardValueType.FIXED_AMOUNT
        cash_reward["object"] = cash_rewards
        return cash_reward

    def _voucher_rewards_details(self, voucher_rewards):
        voucher = voucher_rewards.first()
        return {
            "object": voucher,
            "value_maximum": voucher.value_maximum,
            "value": voucher.value,
            "type": RewardValueType.PERCENTAGE,
        }
