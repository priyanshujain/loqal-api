from re import I
from api.exceptions import ValidationError, ErrorDetail
from api.views import MerchantAPIView
from apps.order.services import CheckRewardAvailable
from api.helpers import run_validator
from apps.order.validators import CheckRewardSerializer
from apps.rewards.options import RewardValueType
from apps.account.dbapi import get_merchant_account_by_uid
from django.utils.translation import gettext as _


class CheckRewardsAvailableAPI(MerchantAPIView):
    def post(self, request):
        data = run_validator(CheckRewardSerializer, self.request_data)
        merchant_id = str(data["merchant_id"])
        merchant = get_merchant_account_by_uid(merchant_uid=merchant_id)
        if not merchant:
            raise ValidationError({
                "detail": ErrorDetail(_("Given merchant is not valid. Please check back and try again."))
            })
        reward_data = CheckRewardAvailable(
            consumer_id=request.consumer_account.id,
            merchant_id=merchant.id,
        ).handle()
        if not reward_data:
            return self.response()
        elif reward_data["type"] == RewardValueType.FIXED_AMOUNT:
            return {
                "type": {
                    "value": RewardValueType.FIXED_AMOUNT.value,
                    "label": RewardValueType.FIXED_AMOUNT.label,
                },
                "value": reward_data["total_available"],
            }
        else:
            return {
                "type": {
                    "value": RewardValueType.PERCENTAGE.value,
                    "label": RewardValueType.PERCENTAGE.label,
                },
                "value_maximum": reward_data["value_maximum"],
                "value": reward_data["value"],
            }