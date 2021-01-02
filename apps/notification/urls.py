from django.urls import path

from apps.notification.views import SubscribePushNoticationAPI

urlpatterns = [
    path(
        "subscribe/",
        SubscribePushNoticationAPI.as_view(),
        name="subscribe_push_notification",
    ),
]
