from .base import urlpatterns as base_urls
from .consumer import urlpatterns as consumer_urls
from .merchant import urlpatterns as merchant_urls

urlpatterns = base_urls + consumer_urls + merchant_urls
