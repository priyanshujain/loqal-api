from django.urls import path

from apps.payment.views.qrcode import (
    CreateQrCodeAPI,
    AssignQrCodeAPI,
    GetAllMerchantQrCodesAPI,
    GetCashierQrCodesAPI,
    GetQrCodeMerchantDetailsAPI,
)

urlpatterns = [
    path("qrcode/create/", CreateQrCodeAPI.as_view(), name="create_qrcode"),
    path("qrcode/assign/", AssignQrCodeAPI.as_view(), name="assign_qrcode"),
    path(
        "merchant/qrcodes/", GetAllMerchantQrCodesAPI.as_view(), name="merchant_qrcodes"
    ),
    path("cashier/qrcode/", GetCashierQrCodesAPI.as_view(), name="cashier_qrcode"),
    path(
        "qrcode/merchant-details/",
        GetQrCodeMerchantDetailsAPI.as_view(),
        name="qrcode_merchant_details",
    ),
]
