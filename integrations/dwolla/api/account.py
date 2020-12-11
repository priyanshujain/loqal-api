"""
This module provides a class for account creation related calls to the dwolla API.
"""

from rest_framework.exceptions import bad_request
from integrations.dwolla.http import Http
from integrations.dwolla.adapters.kyc import get_adapted_kyc_data
from apps.account.options import AccountStatus
from integrations.dwolla.errors import BadRequestError
from integrations.utils.options import RequestStatusTypes


__all__ = "Account"


class MerchantAccountStatusMap:
    unverified = "UNVERIFIED"
    verified = "VERIFIED"
    retry = "RETRY"
    document = "DOCUMENT"
    suspended = "SUSPENDED"


class Account(Http):
    """
    This class provides an interface to the Customers endpoints of the dwolla API.
    """

    def get_account(self, customer_id):
        """
        get customer account
        """

        response = self.get(
            f"/customers/{customer_id}",
            authenticated=True,
            retry=False,
        )
        response = response.json()
        return {"status": getattr(MerchantAccountStatusMap, response["status"])}

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

    def create_merchant_account(self, data):
        """
        Create consumer account
        """

        request_data = get_adapted_kyc_data(data=data)
        try:
            response = self.post(
                "/customers",
                data=request_data,
                authenticated=True,
                retry=False,
            )
        except BadRequestError as err:
            return {
                "status": RequestStatusTypes.ERROR,
                "errors": err.errors,
            }
        
        response_headers = response.headers
        location = response_headers["location"]
        dwolla_customer_id = location.split("/").pop()

        account = self.get_account(customer_id=dwolla_customer_id)
        return {"dwolla_customer_id": dwolla_customer_id, "status": account["status"]}
