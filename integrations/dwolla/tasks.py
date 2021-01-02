from datetime import timedelta

from dateutil import parser
from django.utils import timezone

from apps.provider.models import PaymentProvider, PaymentProviderAuth

__all__ = "store_auth_token"

# TODO: Genralize this according to multiple providers
def store_auth_token(auth_data):
    """
    Store auth token into DB
    """
    provider_obj = PaymentProvider.objects.get(provider_slug="DWOLLA")
    expires_in = int(auth_data["expires_in"]) - 30
    expires_at = timezone.now() + timedelta(seconds=expires_in)
    try:
        provider_auth_obj = provider_obj.paymentproviderauth
        provider_auth_obj.auth_token = auth_data["access_token"]
        provider_auth_obj.expires_at = expires_at
        provider_auth_obj.save()
    except AttributeError:
        PaymentProviderAuth.objects.create(
            provider=provider_obj,
            auth_token=auth_data["access_token"],
            expires_at=expires_at,
        )
