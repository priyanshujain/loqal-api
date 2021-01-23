"""
This module provides a class for account creation related calls to the dwolla API.
"""


import re

from apps.account.options import (AccountCerficationStatus,
                                  DwollaCustomerStatus,
                                  DwollaCustomerVerificationStatus)
from apps.merchant.options import BeneficialOwnerStatus, IndividualDocumentType
from integrations.dwolla.adapters.kyc import (get_adapted_benficial_owner,
                                              get_adapted_kyc_data)
from integrations.dwolla.errors import BadRequestError
from integrations.dwolla.http import Http
from integrations.utils.options import RequestStatusTypes

__all__ = "Account"


class AccountStatusMap:
    unverified = DwollaCustomerStatus.UNVERIFIED
    verified = DwollaCustomerStatus.VERIFIED
    retry = DwollaCustomerStatus.RETRY
    document = DwollaCustomerStatus.DOCUMENT
    suspended = DwollaCustomerStatus.SUSPENDED


class AccountVerificationStatusMap:
    unverified = DwollaCustomerVerificationStatus.UNVERIFIED
    verified = DwollaCustomerVerificationStatus.VERIFIED
    retry = DwollaCustomerVerificationStatus.REVERIFICATION_NEEDED
    document = DwollaCustomerVerificationStatus.DOCUMENT_NEEDED
    suspended = DwollaCustomerVerificationStatus.SUSPENDED


class BeneficialOwnerStatusMap:
    verified = BeneficialOwnerStatus.VERIFIED
    incomplete = BeneficialOwnerStatus.INCOMPLETE
    document = BeneficialOwnerStatus.DOCUMENT_PENDING


class BeneficialOwnerCertificationStatusMap:
    uncertified = AccountCerficationStatus.UNCERTIFIED
    recertify = AccountCerficationStatus.RECERTIFY
    certified = AccountCerficationStatus.CERTIFIED


INDIVIDUAL_DUCUMENT_MAP = {
    IndividualDocumentType.DRIVER_LICENSE: "license",
    IndividualDocumentType.US_PASSPORT: "passport",
    IndividualDocumentType.FOREIGN_PASSPORT: "passport",
    IndividualDocumentType.US_VISA: "other",
    IndividualDocumentType.FEAC: "idCard",
}


class Account(Http):
    """
    This class provides an interface to the Customers endpoints of the dwolla API.
    """

    def get_customer_details(self, customer_id):
        """
        get customer account
        """

        response = self.get(
            f"/customers/{customer_id}",
            authenticated=True,
            retry=False,
        )
        return response.json()

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
        customer_details = self.get_customer_details(
            customer_id=dwolla_customer_id
        )
        return {
            "dwolla_customer_id": dwolla_customer_id,
            "status": getattr(AccountStatusMap, response["status"]),
            "verification_status": getattr(
                AccountVerificationStatusMap, response["status"]
            ),
        }

    def get_customer_account(self):
        """
        get customer account
        """

        response = self.get(
            f"/customers/{self.config.customer_id}",
            authenticated=True,
            retry=False,
        )
        return self.parse_merchant_details_response(response=response.json())

    def parse_merchant_details_response(self, response):
        links = response["_links"]
        is_controller_docs_required = "verify-with-document" in links
        is_business_docs_required = "verify-business-with-document" in links
        is_both_docs_required = (
            "verify-controller-and-business-with-document" in links
        )
        return {
            "dwolla_customer_id": response["id"],
            "status": getattr(AccountStatusMap, response["status"]),
            "verification_status": getattr(
                AccountVerificationStatusMap, response["status"]
            ),
            "is_certification_required": "certify-beneficial-ownership"
            in links,
            "controller_document_required": is_controller_docs_required
            or is_both_docs_required,
            "business_document_required": is_business_docs_required
            or is_both_docs_required,
        }

    def create_merchant_account(self, data, is_update=False):
        """
        Create consumer account
        """

        request_data = get_adapted_kyc_data(data=data)

        endpoint = "/customers"
        if is_update:
            endpoint = f"/customers/{data['dwolla_id']}"
        try:
            response = self.post(
                endpoint,
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
        dwolla_customer_id = location.split("/").pop()
        customer_details = self.get_customer_details(
            customer_id=dwolla_customer_id
        )
        return self.parse_merchant_details_response(response=customer_details)

    def retry_merchant_account(self, data):
        """
        Retry consumer account
        """
        request_data = get_adapted_kyc_data(data=data)
        try:
            response = self.post(
                f"/customers/{self.config.customer_id}",
                data=request_data,
                authenticated=True,
                retry=False,
            )
        except BadRequestError as err:
            return {
                "status": RequestStatusTypes.ERROR,
                "errors": err.api_errors,
            }
        return self.parse_merchant_details_response(response=response.json())

    def upload_customer_document(
        self, document_file, document_type, entity_type
    ):
        """
        Upload verification document for a customer
        """
        if entity_type == "business":
            document_type = "other"
        else:
            document_type = INDIVIDUAL_DUCUMENT_MAP[document_type]
        endpoint = f"/customers/{self.config.customer_id}/documents"
        file = document_file["file"]
        file_name = document_file["file_name"]
        content_type = document_file["content_type"]
        try:
            response = self.post(
                endpoint,
                data={"documentType": document_type},
                files=[
                    ("file", (file_name, open(file.name, "rb"), content_type))
                ],
                custom_content_type="multipart/form-data",
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

    def get_beneficial_owner(self, beneficial_owner_id):
        """
        Get beneficial owner details
        """
        response = self.get(
            f"/beneficial-owners/{beneficial_owner_id}",
            authenticated=True,
            retry=False,
        )
        response = response.json()
        return {
            "dwolla_id": response["id"],
            "status": getattr(
                BeneficialOwnerStatusMap, response["verificationStatus"]
            ),
        }

    def add_beneficial_owner(self, data, is_update=False):
        """
        Add beneficial owner
        """
        request_data = get_adapted_benficial_owner(data=data)

        endpoint = f"customers/{self.config.customer_id}/beneficial-owners"
        if is_update:
            endpoint = f"{endpoint}/{data['dwolla_id']}"
        try:
            response = self.post(
                endpoint,
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
        beneficial_owner_id = location.split("/").pop()

        return self.get_beneficial_owner(
            beneficial_owner_id=beneficial_owner_id
        )

    def upload_ba_document(
        self, beneficial_owner_id, document_file, document_type
    ):
        """
        Upload verification document for beneficial owner
        """
        document_type = INDIVIDUAL_DUCUMENT_MAP[document_type]
        endpoint = f"/beneficial-owners/{beneficial_owner_id}/documents"
        file = document_file["file"]
        file_name = document_file["file_name"]
        content_type = document_file["content_type"]
        try:
            response = self.post(
                endpoint,
                data={"documentType": document_type},
                files=[
                    ("file", (file_name, open(file.name, "rb"), content_type))
                ],
                authenticated=True,
                custom_content_type="multipart/form-data",
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

    def get_ba_cerification_status(self):
        """
        get beneficial owner certifcation status
        """

        endpoint = f"customers/{self.config.customer_id}/beneficial-ownership"
        response = self.get(
            endpoint,
            authenticated=True,
            retry=False,
        )
        response = response.json()
        return {
            "status": getattr(
                BeneficialOwnerCertificationStatusMap, response["status"]
            )
        }

    def certify_beneficial_owner(self):
        """
        Add beneficial owner
        """

        endpoint = f"customers/{self.config.customer_id}/beneficial-ownership"
        try:
            response = self.post(
                endpoint,
                data={"status": "certified"},
                authenticated=True,
                retry=False,
            )
        except BadRequestError as err:
            return {
                "status": RequestStatusTypes.ERROR,
                "errors": err.api_errors,
            }
        response = response.json()
        return {
            "status": getattr(
                BeneficialOwnerCertificationStatusMap, response["status"]
            ),
        }
