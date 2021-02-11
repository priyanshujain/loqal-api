"""
This module provides a class for funding bank account 
creation related calls to the dwolla API.
"""

from apps.banking.options import DwollaFundingSourceStatus
from integrations.dwolla.errors import NotFoundError
from integrations.dwolla.http import Http

__all__ = "Banking"


class DwollaFundingSourceStatusMap:
    verified = DwollaFundingSourceStatus.VERIFIED
    unverified = DwollaFundingSourceStatus.UNVERIFIED


class Banking(Http):
    """
    This class provides an interface to the Customers endpoints of the dwolla API.
    """

    def get_iav_token(self):
        """
        get bank account (Funding source)
        """
        try:
            response = self.get(
                f"/customers/{self.config.customer_id}/iav-token",
                authenticated=True,
                retry=False,
            )
        except NotFoundError:
            return None
        return response.json()
    
    def get_bank_account(self, funding_source_id):
        """
        get bank account (Funding source)
        """
        try:
            response = self.get(
                f"/funding-sources/{funding_source_id}",
                authenticated=True,
                retry=False,
            )
        except NotFoundError:
            return None
        return response.json()

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
        funding_source_details = self.get_bank_account(
            funding_source_id=dwolla_funding_source_id
        )
        return {
            "dwolla_funding_source_id": dwolla_funding_source_id,
            "status": getattr(
                DwollaFundingSourceStatusMap, funding_source_details["status"]
            ),
        }

    def get_bank_accounts(self):
        """
        get bank account (Funding source)
        """
        try:
            response = self.get(
                f"/customers/{self.config.customer_id}/funding-sources",
                authenticated=True,
                retry=False,
            )
        except NotFoundError:
            return None
        return response.json()

    def remove_bank_account(self, funding_source_id):
        """
        remove bank account (Funding source)
        """
        try:
            response = self.post(
                f"/funding-sources/{funding_source_id}",
                data={"removed": True},
                authenticated=True,
                retry=False,
            )
        except NotFoundError:
            return {"is_sucess": False}
        response = response.json()
        if response["removed"] == True:
            return {"is_success": True}
        else:
            return {"is_success": False}

    def update_bank_account(self, funding_source_id):
        """
        remove bank account (Funding source)
        """
        try:
            response = self.post(
                f"/funding-sources/{funding_source_id}",
                authenticated=True,
                retry=False,
            )
        except NotFoundError:
            return None
        return response.json()
