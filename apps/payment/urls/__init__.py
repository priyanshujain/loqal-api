from .payment import urlpatterns as payment_urls
from .qrcode import urlpatterns as qrcode_urls


urlpatterns = payment_urls + qrcode_urls