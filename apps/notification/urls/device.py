from django.urls import path

from apps.notification.views.device import (SubscribePushNoticationAPI,
                                            UnSubscribePushNoticationAPI)

urlpatterns = [
    path(
        "subscribe/",
        SubscribePushNoticationAPI.as_view(),
        name="subscribe_push_notification",
    ),
    path(
        "unsubscribe/",
        UnSubscribePushNoticationAPI.as_view(),
        name="unsubscribe_push_notification",
    ),
]
