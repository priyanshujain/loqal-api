"""
This module provides a class for authentication related calls to the afex API.
"""

from integrations.dwolla.errors import BadRequestError
from integrations.dwolla.http import Http
from integrations.dwolla.tasks import store_auth_token

__all__ = "Auth"


class Auth(Http):
    """
    This class provides an interface to the Authentication endpoints of the afex API.
    """

    def authenticate(self):
        """
        Exchange API-Key and API-Password for a temporary Auth Token.
        """
        try:
            response = self.post(
                "/token",
                {
                    "client_id": self.config.client_id,
                    "client_secret": self.config.client_secret,
                    "grant_type": "client_credentials",
                },
                custom_content_type="application/x-www-form-urlencoded",
                authenticated=False,
                retry=True,
            )
            content = response.json()
            store_auth_token(content)
            return content
        except BadRequestError:
            return {"auth_token": ""}
