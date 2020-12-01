"""
This module provides a Client class for authentication related calls to the Dwolla API.
"""


import requests

from apps.provider.options import APIEnvironmentTypes
from integrations.dwolla.api.auth import Auth

__all__ = "Config"


class Config(object):
    """
    API Configuration Object. Keeps track of Credentials, Auth Token and API Environment.
    """

    _auth_token = None
    _session = None

    ENV_PROD = APIEnvironmentTypes.PRODUCTION
    ENV_SANDBOX = APIEnvironmentTypes.SANDBOX

    ENVIRONMENT_URLS = {
        ENV_PROD: {
            "auth": {"v1": "https://accounts.dwolla.com/auth"},
            "token": {"v1": "https://api.dwolla.com/token",},
            "api": {"v1": "https://api.dwolla.com",},
            "type": "production",
        },
        ENV_SANDBOX: {
            "auth": {"v1": "https://accounts-sandbox.dwolla.com/auth"},
            "token": {"v1": "https://api-sandbox.dwolla.com/token",},
            "api": {"v1": "https://api-sandbox.dwolla.com",},
        },
        "type": "sandbox",
    }

    def __init__(self, provider_config, client_config, request_tracker):
        """
        For dwolla

        api_password => client_secret
        api_key = client_id
        """
        self.client_secret = provider_config.get("api_password")
        self.client_id = provider_config.get("api_key")
        self.client_api_key = client_config.get("api_key", None)
        self.environment = provider_config.get("api_environment")
        self._auth_token = provider_config.get("auth_token", None)
        self.request_tracker = request_tracker

    @property
    def auth_token(self):
        """
        Getter for the Auth Token. Generates one if there is None.
        """
        if self._auth_token is None:
            if self.client_secret is None:
                raise RuntimeError("client_secret must be set")
            if self.client_id is None:
                raise RuntimeError("client_id must be set")

            self._auth_token = Auth(self).authenticate()["access_token"]
        return self._auth_token

    @property
    def session(self):
        """
        psp request session
        """
        if not self._session:
            self._session = requests.Session()
        return self._session

    def reauthenticate(self):
        """
        Force generation of a new auth token.
        """
        if self.client_secret is None:
            raise RuntimeError("client_secret must be set")
        if self.client_id is None:
            raise RuntimeError("client_id must be set")

        self._auth_token = Auth(self).authenticate()["access_token"]

    def environment_url(self, api_type="api", version="v1"):
        """
        Get API url for request type.
        """
        if self.environment not in self.ENVIRONMENT_URLS:
            raise RuntimeError(
                "%s is not a valid environment name" % self.environment
            )

        return self.ENVIRONMENT_URLS[self.environment][api_type][version]
