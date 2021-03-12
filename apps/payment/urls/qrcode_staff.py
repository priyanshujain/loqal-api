from django.urls import path

from apps.payment.views.qrcode_staff import (AssignQrCodeAPI,
                                             GetAllMerchantQrCodesAPI,
                                             GetQrCodeImageAPI)

urlpatterns = [
    path(
        "merchant/<uuid:merchant_id>/qrcode/assign/",
        AssignQrCodeAPI.as_view(),
        name="staff_assign_qrcode",
    ),
    path(
        "merchant/<uuid:merchant_id>/qrcodes/",
        GetAllMerchantQrCodesAPI.as_view(),
        name="staff_merchant_qrcodes",
    ),
    path(
        "merchant/<uuid:merchant_id>/qrcode/image/",
        GetQrCodeImageAPI.as_view(),
        name="staff_qrcode_image",
    ),
]
