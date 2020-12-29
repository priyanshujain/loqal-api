from .merchant_payment import urlpatterns as merchant_payment_urls
from .payment import urlpatterns as payment_urls
from .qrcode import urlpatterns as qrcode_urls
from .refund import urlpatterns as refund_urls
from .dispute import urlpatterns as dispute_urls

urlpatterns = payment_urls + qrcode_urls + merchant_payment_urls + refund_urls + dispute_urls
