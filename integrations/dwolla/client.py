"""
This module provides a the Client interface to the AFEX APIs.
"""

from integrations.dwolla.api import *
from integrations.dwolla.api.account import Account
from integrations.dwolla.config import Config

__all__ = "Client"


class Client(object):
    """
    The Client interfacing to the AFEX APIs.
    """

    _auth_client = None
    _account_client = None

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
