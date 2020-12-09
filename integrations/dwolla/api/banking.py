"""
This module provides a class for funding bank account 
creation related calls to the dwolla API.
"""

from integrations.dwolla.http import Http

__all__ = "Banking"


class Banking(Http):
    """
    This class provides an interface to the Customers endpoints of the dwolla API.
    """

    def create_bank_account(self, data):
        """
        Create bank account (Funding source)
        """
        request_data = {
            "plaidToken": data["processor_token"],
            "name": data["account_name"],
        }
        response = self.post(
            f"/customers/{self.config.customer_id}/funding-sources",
            data=request_data,
            authenticated=True,
            retry=False,
        )
        response_headers = response.headers
        location = response_headers["location"]
        dwolla_funding_source_id = location.split("/").pop()
        return {"dwolla_funding_source_id": dwolla_funding_source_id}
