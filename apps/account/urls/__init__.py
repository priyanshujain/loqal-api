from .consumer import urlpatterns as consumer_urls
from .merchant import urlpatterns as merchant_urls
from .staff import urlpatterns as staff_urls

urlpatterns = merchant_urls + consumer_urls + staff_urls
