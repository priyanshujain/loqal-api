from .merchant_payment import urlpatterns as merchant_payment_urls
from .payment import urlpatterns as payment_urls
from .qrcode import urlpatterns as qrcode_urls

urlpatterns = payment_urls + qrcode_urls + merchant_payment_urls
