"""
This module provides a class for payments 
creation related calls to the dwolla API.
"""

from apps.payment.options import TransactionStatus
from integrations.dwolla.errors import BadRequestError, NotFoundError
from integrations.dwolla.http import Http

__all__ = "Payment"


class TransactionStatusMap:
    pending = TransactionStatus.PENDING
    processed = TransactionStatus.PROCESSED
    failed = TransactionStatus.FAILED
    cancelled = TransactionStatus.CANCELLED


class Payment(Http):
    """
    This class provides an interface to the Transfers endpoints of the dwolla API.
    """

    # TODO: Integrate achDetails and addenda object
    # TODO: Integrate clearing JSON object

    def funding_source_url(self, bank_account_dwolla_id):
        """
        Dwolla endpoint for founding-sources.
        """

        return {
            "href": f"{self.config.environment_url()}/funding-sources/{bank_account_dwolla_id}"
        }

    def cusotmer_url(self, account_dwolla_id):
        """
        Dwolla endpoint for cusotmers.
        """

        return {
            "href": f"{self.config.environment_url()}/customers/{account_dwolla_id}"
        }

    def get_payment_details(self, transfer_id):
        """
        Dwolla endpoint for get transfer details
        """

        response = self.get(
            f"/transfers/{transfer_id}",
            authenticated=True,
            retry=False,
        )
        response = response.json()
        return response

    def get_payment_fees(self, transfer_id):
        """
        Dwolla endpoint for get transfer fee details
        """

        response = self.get(
            f"/transfers/{transfer_id}/fees",
            authenticated=True,
            retry=False,
        )
        response = response.json()
        return response

    def get_payment_failure(self, transfer_id):
        """
        Dwolla endpoint for get transfer fee details
        """

        try:
            response = self.get(
                f"/transfers/{transfer_id}/failure",
                authenticated=True,
                retry=False,
            )
        except NotFoundError:
            return None
        response = response.json()
        return response

    def create_new_payment(self, data):
        """
        Create new payment (transfer)
        """

        sender_bank_account_dwolla_id = data["sender_bank_account_dwolla_id"]
        receiver_bank_account_dwolla_id = data[
            "receiver_bank_account_dwolla_id"
        ]
        fee_bearer_dwolla_id = data["fee_bearer_dwolla_id"]
        correlation_id = data["correlation_id"]
        currency = data["currency"]
        amount = data["amount"]
        fee_currency = data["fee_currency"]
        fee_amount = data["fee_amount"]

        request_data = {
            "_links": {
                "source": self.funding_source_url(
                    bank_account_dwolla_id=sender_bank_account_dwolla_id
                ),
                "destination": self.funding_source_url(
                    bank_account_dwolla_id=receiver_bank_account_dwolla_id
                ),
            },
            "correlationId": correlation_id,
            "amount": {"currency": currency, "value": amount},
            "fees": [
                {
                    "_links": {
                        "charge-to": self.cusotmer_url(
                            account_dwolla_id=fee_bearer_dwolla_id
                        )
                    },
                    "amount": {"value": fee_amount, "currency": fee_currency},
                }
            ],
        }

        response = self.post(
            f"/transfers",
            data=request_data,
            authenticated=True,
            retry=False,
        )

        response_headers = response.headers
        location = response_headers["location"]
        dwolla_transfer_id = location.split("/").pop()
        payment_details = self.get_payment_details(
            transfer_id=dwolla_transfer_id
        )
        return {
            "dwolla_transfer_id": dwolla_transfer_id,
            "status": getattr(TransactionStatusMap, payment_details["status"]),
            "individual_ach_id": payment_details.get("individualAchId", None),
        }
