from django.urls import path

from apps.payment.views.dispute import (ChangeDisputeStatusAPI,
                                        CloseDisputeAPI, GetAllDisputeAPI)
from apps.payment.views.staff import (ConsumerPaymentLimitAPI,
                                      GetAllQrCodesAPI, GetQrCodeImageAPI,
                                      MerchantReceiveLimitAPI)

urlpatterns = [
    path(
        "staff/disputes/<str:dispute_id>/close/",
        CloseDisputeAPI.as_view(),
        name="close_dispute",
    ),
    path(
        "staff/disputes/<str:dispute_id>/update/",
        ChangeDisputeStatusAPI.as_view(),
        name="update_dispute",
    ),
    path(
        "staff/disputes/",
        GetAllDisputeAPI.as_view(),
        name="all_disputes",
    ),
    path(
        "staff/qrcodes/<str:qrcode_id>/",
        GetQrCodeImageAPI.as_view(),
        name="qrcode_img_staff",
    ),
    path(
        "staff/payment-limit/merchant/<uuid:merchant_id>/",
        MerchantReceiveLimitAPI.as_view(),
        name="staff_merchant_receive_limit",
    ),
    path(
        "staff/payment-limit/consumer/<uuid:consumer_id>/",
        ConsumerPaymentLimitAPI.as_view(),
        name="staff_consumer_payment_limit",
    ),
    path(
        "staff/qrcodes/",
        GetAllQrCodesAPI.as_view(),
        name="all_qrcodes",
    ),
]
