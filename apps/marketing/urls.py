from django.urls import path

from apps.marketing.views.consumer import GetConsumerCampaignsAPI
from apps.marketing.views.merchant import GetMerchantCampaignsAPI
from apps.marketing.views.staff import (CreateCampaignAPI, GetCampaignsAPI,
                                        UpdateCampaignAPI)

urlpatterns = [
    path(
        "consumer/campaigns/",
        GetConsumerCampaignsAPI.as_view(),
        name="consumer_campaigns",
    ),
    path(
        "merchant/campaigns/",
        GetMerchantCampaignsAPI.as_view(),
        name="merchant_campaigns",
    ),
    path(
        "staff/campaigns/create/",
        CreateCampaignAPI.as_view(),
        name="create_campaign",
    ),
    path(
        "staff/campaigns/update/",
        UpdateCampaignAPI.as_view(),
        name="update_campaign",
    ),
    path(
        "staff/campaigns/",
        GetCampaignsAPI.as_view(),
        name="staff_campaigns",
    ),
]
