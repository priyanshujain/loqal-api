from .device import urlpatterns as device_urls
from .staff_payment import urlpatterns as staff_payment_urls

urlpatterns = device_urls + staff_payment_urls
