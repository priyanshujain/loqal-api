"""
This module provides a class for account creation related calls to the afex API.
"""

from integrations.dwolla.http import Http

__all__ = "Account"


class Account(Http):
    """
    This class provides an interface to the Customers endpoints of the afex API.
    """

    def create_consumer_account(self):
        """
        Create consumer account
        """
        response = self.post("/customers", authenticated=True, retry=False,)
        response_headers = response.headers
        location = response_headers["location"]
        dwolla_customer_id = location.split("/").pop()
        return {"dwolla_customer_id": dwolla_customer_id}
