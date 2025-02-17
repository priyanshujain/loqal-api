from .dispute import urlpatterns as dispute_urls
from .merchant_payment import urlpatterns as merchant_payment_urls
from .payment import urlpatterns as payment_urls
from .pos import urlpatterns as pos_urls
from .qrcode import urlpatterns as qrcode_urls
from .qrcode_staff import urlpatterns as qrcode_staff_urls
from .refund import urlpatterns as refund_urls
from .staff import urlpatterns as staff_urls

urlpatterns = (
    payment_urls
    + qrcode_urls
    + merchant_payment_urls
    + refund_urls
    + dispute_urls
    + staff_urls
    + qrcode_staff_urls
    + pos_urls
)
