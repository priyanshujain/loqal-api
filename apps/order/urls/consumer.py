from django.urls import path

from apps.order.views.consumer import (CheckRewardsAvailableAPI,
                                       MerchantRewardDetailsAPI,
                                       RewardedMerchantsAPI)

urlpatterns = [
    path(
        "consumer/reward-merchants/",
        RewardedMerchantsAPI.as_view(),
        name="reward_merchants",
    ),
    path(
        "consumer/available-rewards/<uuid:merchant_id>/",
        CheckRewardsAvailableAPI.as_view(),
        name="available_rewards",
    ),
    path(
        "consumer/reward-details/<uuid:merchant_id>/",
        MerchantRewardDetailsAPI.as_view(),
        name="reward_details",
    ),
]
