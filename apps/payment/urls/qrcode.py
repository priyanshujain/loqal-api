from django.urls import path

from apps.payment.views.qrcode import (AssignQrCodeAPI, CreateQrCodeAPI,
                                       GetAllMerchantQrCodesAPI,
                                       GetCashierQrCodesAPI, GetQrCodeImageAPI,
                                       GetQrCodeMerchantDetailsAPI)

urlpatterns = [
    path("qrcode/create/", CreateQrCodeAPI.as_view(), name="create_qrcode"),
    path("qrcode/assign/", AssignQrCodeAPI.as_view(), name="assign_qrcode"),
    path(
        "merchant/qrcodes/",
        GetAllMerchantQrCodesAPI.as_view(),
        name="merchant_qrcodes",
    ),
    path(
        "cashier/qrcode/",
        GetCashierQrCodesAPI.as_view(),
        name="cashier_qrcode",
    ),
    path(
        "qrcode/merchant-details/",
        GetQrCodeMerchantDetailsAPI.as_view(),
        name="qrcode_merchant_details",
    ),
    path(
        "qrcode/image/",
        GetQrCodeImageAPI.as_view(),
        name="qrcode_image",
    ),
]
