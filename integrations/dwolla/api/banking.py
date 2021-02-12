"""
This module provides a class for funding bank account 
creation related calls to the dwolla API.
"""

from apps.banking.options import DwollaFundingSourceStatus
from integrations.dwolla.errors import (BadRequestError, ForbiddenError,
                                        NotFoundError)
from integrations.dwolla.errors.api import BadRequestError
from integrations.dwolla.http import Http
from integrations.utils.options import RequestStatusTypes

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
            response = self.post(
                f"/customers/{self.config.customer_id}/iav-token",
                authenticated=True,
                retry=False,
            )
        except NotFoundError:
            return None
        response = response.json()
        return {"token": response["token"]}

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
        data = response.json()
        customer_dwolla_id = (
            data["_links"]["customer"]["href"].split("/").pop()
        )

        links = data["_links"]
        micro_deposit_verification_available = "verify-micro-deposits" in links
        is_micro_deposit = "micro-deposits" in links

        return {
            "status": getattr(DwollaFundingSourceStatusMap, data["status"]),
            "name": data["name"],
            "bank_name": data["bankName"],
            "dwolla_id": data["id"],
            "bank_account_type": data["bankAccountType"],
            "type": data["type"],
            "removed": data["removed"],
            "customer_dwolla_id": customer_dwolla_id,
            "micro_deposit_verification_available": micro_deposit_verification_available,
            "is_micro_deposit": is_micro_deposit,
        }

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
            "status": funding_source_details.get("status"),
        }

    def verify_micro_deposit(self, data):
        """
        Create bank account (Funding source)
        """
        request_data = {
            "id": data["dwolla_id"],
            "amount1": {
                "value": str(data["amount1"]),
                "currency": data["currency"],
            },
            "amount2": {
                "value": str(data["amount2"]),
                "currency": data["currency"],
            },
        }
        errors = []
        try:
            response = self.post(
                f"/funding-sources/{data['dwolla_id']}/micro-deposits",
                data=request_data,
                authenticated=True,
                retry=False,
            )
            if response.status_code == 200:
                return self.get_bank_account(
                    funding_source_id=data["dwolla_id"]
                )
            if response.status_code == 202:
                errors = [
                    {
                        "message": (
                            "Micro-deposits have not have not settled "
                            "to destination bank. A Customer can verify these "
                            "amounts after micro-deposits have processed to "
                            "their bank."
                        )
                    }
                ]
        except BadRequestError as err1:
            errors = err1.api_errors
        except ForbiddenError as err2:
            errors = err2.api_errors

        if errors:
            errors = [error["message"] for error in errors]

        if errors:
            return {"status": RequestStatusTypes.ERROR, "errors": errors}

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
        update bank account (Funding source)
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
