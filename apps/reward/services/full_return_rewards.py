from decimal import Decimal

from api.services import ServiceBase
from apps.reward.options import RewardValueType

from .return_rewards import ReturnRewards

__all__ = ("FullReturnRewards",)


class FullReturnRewards(ServiceBase):
    def __init__(
        self,
        reward_usage,
    ):
        self.reward_usage = reward_usage

    def handle(self):
        reward_usage = self.reward_usage
        reward_value_type = reward_usage.reward_value_type
        if reward_value_type == RewardValueType.PERCENTAGE:
            return ReturnRewards(
                return_reward_value=Decimal(0.0),
                updated_reward_value=Decimal(0.0),
                reclaim_reward_value=reward_usage.total_amount,
                reward_usage=reward_usage,
            ).handle()
        else:
            return ReturnRewards(
                return_reward_value=reward_usage.total_amount,
                updated_reward_value=Decimal(0.0),
                reclaim_reward_value=Decimal(0.0),
                reward_usage=reward_usage,
            ).handle()
