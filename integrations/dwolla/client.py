"""
This module provides a the Client interface to the Dwolla APIs.
"""

from integrations.dwolla.api import Account, Auth, Banking, Payment, Reference
from integrations.dwolla.config import Config

__all__ = "Client"


class Client(object):
    """
    The Client interfacing to the Dwolla APIs.
    """

    _auth_client = None
    _account_client = None
    _banking_client = None
    _payment_client = None
    _reference_client = None

    def __init__(self, provider_config, client_config, request_tracker):
        self.config = Config(provider_config, client_config, request_tracker)

    def authenticate(self):
        """
        Generate an auth token an store it in the config.
        """
        response = self.auth.authenticate()
        self.config.auth_token = response["auth_token"]

    def close_session(self):
        """
        Terminate the Auth Token validity.
        """
        self.config.auth_token = None
        return True

    @property
    def auth(self):
        """
        Get the Authentication client.
        """
        if self._auth_client is None:
            self._auth_client = Auth(self.config)
        return self._auth_client

    @property
    def account(self):
        """
        Get the account client.
        """
        if self._account_client is None:
            self._account_client = Account(self.config)
        return self._account_client

    @property
    def banking(self):
        """
        Get the banking client.
        """
        if self._banking_client is None:
            self._banking_client = Banking(self.config)
        return self._banking_client

    @property
    def payment(self):
        """
        Get the payment client.
        """
        if self._payment_client is None:
            self._payment_client = Payment(self.config)
        return self._payment_client

    @property
    def reference(self):
        """
        Get the reference client.
        """
        if self._reference_client is None:
            self._reference_client = Reference(self.config)
        return self._reference_client
