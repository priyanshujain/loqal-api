from .consumer import urlpatterns as consumer_urls
from .merchant import urlpatterns as merchant_urls

urlpatterns = consumer_urls + merchant_urls
