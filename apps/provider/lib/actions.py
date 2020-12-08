from django.conf import settings
from django.utils import timezone

from api.exceptions import ErrorDetail, ValidationError
from apps.account.dbapi import get_account
from apps.provider.dbapi import get_provider_cred
from apps.provider.lib.client import APIClient
from apps.tracking.clients import PspAPIRequestTracker
from integrations.clients import CLIENT_CLASSES
from integrations.options import IntegratedProviders
from integrations.utils.options import CommonStatusTypes


class ProviderAPIActionBase(object):
    """Base client for using provider APIs"""

    _client = None
    _error = None
    payment_account = None
    provider = None

    def __init__(self, account_id, provider_slug=IntegratedProviders.DWOLLA):
        self.account_id = account_id
        self.provider_slug = provider_slug

    def get_errors(self, response):
        # FIX: response should be always dict
        if isinstance(response, list):
            return None

        status = response.get("status", "")
        if status == CommonStatusTypes.ERROR:
            self._error = True
            return {
                "errors": response.get("errors", ""),
                "data": response.get("data", {}),
            }
        return None

    def _get_provider_config(self):
        provider_cred_obj = get_provider_cred(
            provider_slug=self.provider_slug, api_environment=settings.API_ENV
        )
        self.provider = provider_cred_obj.provider

        if not provider_cred_obj:
            raise ValidationError(
                {"detail": ErrorDetail("Provider config not found.")}
            )

        config = {
            "api_environment": provider_cred_obj.api_environment,
            "api_password": provider_cred_obj.api_password,
            "api_key": provider_cred_obj.api_key,
            "api_login_id": provider_cred_obj.api_login_id,
        }
        try:
            provider_auth_obj = provider_cred_obj.provider.paymentproviderauth
            if timezone.now() < provider_auth_obj.expires_at:
                config["auth_token"] = provider_auth_obj.auth_token
            return config
        except AttributeError:
            return config

    def _get_client_config(self):
        config = {}
        account = get_account(account_id=self.account_id)
        config["customer_id"] = account.dwolla_id
        return config

    def _get_client(self):
        provider_config = self._get_provider_config()
        client_config = self._get_client_config()
        client_class = CLIENT_CLASSES[self.provider_slug]

        request_tracker = PspAPIRequestTracker(
            account_id=self.account_id, provider_id=self.provider.id
        )
        psp_client = client_class(
            provider_config=provider_config,
            client_config=client_config,
            request_tracker=request_tracker,
        )
        self._client = APIClient(psp_client=psp_client)
        return self._client

    @property
    def client(self):
        return self._get_client()

    @property
    def payment_account_id(self):
        if self.payment_account:
            return self.payment_account.id
        return None
