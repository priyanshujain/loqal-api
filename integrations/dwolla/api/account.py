"""
This module provides a class for account creation related calls to the afex API.
"""

from integrations.dwolla.adapters.account import CreateConsumerAccountAdapter
from integrations.dwolla.http import Http

__all__ = "Account"


class Account(Http):
    """
    This class provides an interface to the Customers endpoints of the afex API.
    """

    def create_consumer_account(self, data):
        """
        Create consumer account
        """
        data = CreateConsumerAccountAdapter().adapt(data=data)
        response = self.post(
            "/customers", data=data, authenticated=True, retry=False,
        )
        response_headers = response.headers
        location = response_headers["location"]
        dwolla_customer_id = location.split("/").pop()
        return {"dwolla_customer_id": dwolla_customer_id}
