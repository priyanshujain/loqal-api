from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.account.options import AccountCerficationStatus, DwollaCustomerStatus
from apps.provider.lib.actions import ProviderAPIActionBase

from .certify_ownership import CertifyDwollaMerchantAccount

__all__ = ("GetMerchantAccountStatus",)


class GetMerchantAccountStatus(ServiceBase):
    def __init__(self, merchant):
        self.merchant = merchant

    def handle(self):
        merchant = self.merchant
        account = merchant.account
        dwolla_response = DwollaGetAccountAPIAction(
            account_id=account.id
        ).get()
        dwolla_customer_id = dwolla_response["dwolla_customer_id"]
        dwolla_status = dwolla_response["status"]
        dwolla_verification_status = dwolla_response["verification_status"]
        is_certification_required = dwolla_response[
            "is_certification_required"
        ]
        controller_document_required = dwolla_response[
            "controller_document_required"
        ]
        business_document_required = dwolla_response[
            "business_document_required"
        ]

        account.add_dwolla_id(dwolla_id=dwolla_customer_id, save=False)
        if dwolla_status == DwollaCustomerStatus.DOCUMENT:
            dwolla_verification_status = None
        account.update_status(
            status=dwolla_status,
            verification_status=dwolla_verification_status,
        )
        account.update_certification_required(
            required=is_certification_required
        )
        if (
            dwolla_status == DwollaCustomerStatus.VERIFIED
            and self.merchant.account.is_certification_required
            and self.merchant.account.certification_status
            != AccountCerficationStatus.CERTIFIED
        ):
            CertifyDwollaMerchantAccount(merchant=self.merchant).handle()

        if controller_document_required:
            controller = merchant.controller_details
            controller.update_verification_document_required(required=True)

        if business_document_required:
            incorporation_details = merchant.incorporation_details
            incorporation_details.update_verification_document_required(
                required=True
            )
        return account


class DwollaGetAccountAPIAction(ProviderAPIActionBase):
    def get(self):
        response = self.client.account.get_customer_account()
        if self.get_errors(response):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "KYC service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return {
            "status": response["data"].get("status"),
            "verification_status": response["data"].get("verification_status"),
            "dwolla_customer_id": response["data"].get("dwolla_customer_id"),
            "is_certification_required": response["data"].get(
                "is_certification_required"
            ),
            "controller_document_required": response["data"].get(
                "controller_document_required"
            ),
            "business_document_required": response["data"].get(
                "business_document_required"
            ),
        }
