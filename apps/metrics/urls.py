from django.urls import path

from apps.metrics.views.consumer import (ConsumerMetricsAPI,
                                         CreateSocialShareAPI)
from apps.metrics.views.merchant import (CreateConsumerRatingAPI,
                                         MerchantMetricsAPI)

urlpatterns = [
    path(
        "consumer/social-share/",
        CreateSocialShareAPI.as_view(),
        name="create_social_share",
    ),
    path(
        "consumer/metrics/",
        ConsumerMetricsAPI.as_view(),
        name="consumer_metrics",
    ),
    path(
        "merchant/metrics/",
        MerchantMetricsAPI.as_view(),
        name="merchant_metrics",
    ),
    path(
        "merchant/transaction/consumer-rating/",
        CreateConsumerRatingAPI.as_view(),
        name="create_consumer_rating",
    ),
]
