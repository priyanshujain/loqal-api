"""
This module provides a class for funding bank account 
creation related calls to the dwolla API.
"""

from integrations.dwolla.errors import BadRequestError
from integrations.dwolla.http import Http
from integrations.utils.options import RequestStatusTypes

__all__ = "Management"


class Management(Http):
    """
    This class provides an interface to the management endpoints of the dwolla API.
    """

    def create_webhook(self, data):
        """
        Create webhook
        """
        request_data = {
            "url": data["webhook_url"],
            "secret": data["webhook_secret"],
        }
        try:
            response = self.post(
                f"/webhook-subscriptions",
                data=request_data,
                authenticated=True,
                retry=False,
            )
        except BadRequestError as err:
            return {
                "status": RequestStatusTypes.ERROR,
                "errors": err.api_errors,
            }
        response_headers = response.headers
        location = response_headers["location"]
        dwolla_id = location.split("/").pop()
        return {"dwolla_id": dwolla_id}

    def get_webhook(self, webhook_id):
        """
        get webhook
        """

        response = self.get(
            f"/webhook-subscriptions/{webhook_id}",
            authenticated=True,
            retry=False,
        )
        response = response.json()
        return response
