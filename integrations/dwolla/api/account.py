"""
This module provides a class for account creation related calls to the dwolla API.
"""

from integrations.dwolla.http import Http

__all__ = "Account"


class Account(Http):
    """
    This class provides an interface to the Customers endpoints of the dwolla API.
    """

    def create_consumer_account(self, data):
        """
        Create consumer account
        """

        request_data = {
            "firstName": data["first_name"],
            "lastName": data["last_name"],
            "email": data["email"],
            "ipAddress": data["ip_address"],
        }
        response = self.post(
            "/customers",
            data=request_data,
            authenticated=True,
            retry=False,
        )
        response_headers = response.headers
        location = response_headers["location"]
        dwolla_customer_id = location.split("/").pop()
        return {"dwolla_customer_id": dwolla_customer_id}
