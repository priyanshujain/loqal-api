from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.account.dbapi import get_merchant_account
from apps.account.options import (AccountCerficationStatus,
                                  DwollaCustomerStatus,
                                  DwollaCustomerVerificationStatus)
from apps.merchant.dbapi import (get_account_member_by_user_id,
                                 update_beneficial_owner_status)
from apps.merchant.options import BeneficialOwnerStatus, BusinessTypes
from apps.merchant.serializers import OnboardingDataSerializer
from apps.provider.lib.actions import ProviderAPIActionBase

__all__ = ("CreateDwollaMerchantAccount",)


class CreateDwollaMerchantAccount(ServiceBase):
    is_all_verified = True

    def __init__(self, merchant_id, user_id, ip_address):
        self.merchant_id = merchant_id
        self.user_id = user_id
        self.ip_address = ip_address

    def handle(self):
        data, merchant = self._prepare_data()
        merchant = self._create_dwolla_account(data=data, merchant=merchant)
        if (
            self.is_all_verified
            and merchant.account.is_certification_required
            and merchant.account.certification_status
            != AccountCerficationStatus.CERTIFIED
        ):
            self._certify_beneficial_owners(merchant=merchant)
        return merchant

    def _prepare_data(self):
        merchant = get_merchant_account(merchant_id=self.merchant_id)
        data = OnboardingDataSerializer(merchant).data
        assert self._validate_data(data=data, merchant=merchant)
        merchant_member = get_account_member_by_user_id(user_id=self.user_id)
        data["incorporation_details"]["user"] = {
            "first_name": merchant_member.user.first_name,
            "last_name": merchant_member.user.last_name,
            "email": merchant_member.user.email,
        }
        data["incorporation_details"]["ip_address"] = self.ip_address
        data["company_email"] = merchant_member.user.email
        return data, merchant

    def _validate_data(self, data, merchant):
        if not (data["incorporation_details"] and data["controller_details"]):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Please provide incorporation details and controller details."
                        )
                    )
                }
            )
        account = merchant.account
        if account.dwolla_customer_status == DwollaCustomerStatus.DOCUMENT:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Merchant has already been submitted for KYC, "
                            "addition documents are required for identification."
                        )
                    )
                }
            )
        if account.dwolla_customer_status == DwollaCustomerStatus.SUSPENDED:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "The account has been suspended, please contact our support team."
                        )
                    )
                }
            )
        if account.dwolla_customer_status == DwollaCustomerStatus.DEACTIVATED:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "The account has been deactivated, please contact our support team."
                        )
                    )
                }
            )
        return True

    def _create_dwolla_account(self, data, merchant):
        merchant_account_data = {
            "incorporation_details": data["incorporation_details"],
            "controller_details": data["controller_details"],
        }
        account = merchant.account
        is_account_update = False
        if account.dwolla_customer_status == DwollaCustomerStatus.RETRY:
            is_account_update = True
            merchant_account_data["dwolla_id"] = account.dwolla_id
        elif account.dwolla_customer_status == DwollaCustomerStatus.VERIFIED:
            self._create_beneficial_owner(
                account_id=account.id,
                data=data,
            )
        if is_account_update or (
            account.dwolla_customer_status == DwollaCustomerStatus.NOT_SENT
        ):
            dwolla_response = DwollaCreateMerchantAccountAPIAction(
                account_id=account.id
            ).create(data=merchant_account_data, is_update=is_account_update)
            merchant.update_company_email(email=data["company_email"])
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
            if (
                account.dwolla_customer_status == DwollaCustomerStatus.RETRY
                and dwolla_status == DwollaCustomerStatus.RETRY
            ):
                dwolla_status = DwollaCustomerStatus.SUSPENDED
                dwolla_verification_status = (
                    DwollaCustomerVerificationStatus.SUSPENDED
                )
            account.update_status(
                status=dwolla_status,
                verification_status=dwolla_verification_status,
            )
            account.update_certification_required(
                required=is_certification_required
            )
            if dwolla_status != DwollaCustomerStatus.VERIFIED:
                self.is_all_verified = False

            if controller_document_required:
                controller = merchant.controller_details
                controller.update_verification_document_required(required=True)

            if business_document_required:
                incorporation_details = merchant.incorporation_details
                incorporation_details.update_verification_document_required(
                    required=True
                )

            if (
                merchant_account_data["incorporation_details"]["business_type"]
                != BusinessTypes.SOLE_PROPRIETORSHIP
            ):
                self._create_beneficial_owner(
                    account_id=account.id,
                    data=data,
                )
        return merchant

    def _create_beneficial_owner(self, account_id, data):
        beneficial_owners = data["beneficial_owners"]
        for beneficial_owner in beneficial_owners:
            is_ba_update = False
            if beneficial_owner["status"] == BeneficialOwnerStatus.VERIFIED:
                continue
            if (
                beneficial_owner["status"]
                == BeneficialOwnerStatus.DOCUMENT_PENDING
            ):
                continue
            if beneficial_owner["status"] == BeneficialOwnerStatus.INCOMPLETE:
                is_ba_update = True
            ba_response = DwollaAddBeneficialOwnerAPIAction(
                account_id=account_id
            ).create(
                data=beneficial_owner,
                is_update=is_ba_update,
            )
            status = ba_response["status"]
            update_beneficial_owner_status(
                beneficial_owner_id=beneficial_owner["id"],
                dwolla_id=ba_response["dwolla_id"],
                status=status,
            )
            if status != BeneficialOwnerStatus.VERIFIED:
                self.is_all_verified = False

    def _certify_beneficial_owners(self, merchant):
        certification = DwollaCertifyBeneficialOwnerAPIAction(
            account_id=merchant.account.id
        ).certify()
        merchant.account.update_certification_status(
            status=certification["status"]
        )


class DwollaCreateMerchantAccountAPIAction(ProviderAPIActionBase):
    def create(self, data, is_update=False):
        dwolla_merchant_account_fn = (
            self.client.account.create_merchant_account
        )
        if is_update:
            dwolla_merchant_account_fn = (
                self.client.account.retry_merchant_account
            )

        response = dwolla_merchant_account_fn(data=data)
        if self.get_errors(response):
            raise ProviderAPIException(
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


class DwollaAddBeneficialOwnerAPIAction(ProviderAPIActionBase):
    def create(self, data, is_update=False):
        response = self.client.account.add_beneficial_owner(
            data=data,
            is_update=is_update,
        )
        if self.get_errors(response):
            raise ProviderAPIException(
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
            "dwolla_id": response["data"].get("dwolla_id"),
        }


class DwollaCertifyBeneficialOwnerAPIAction(ProviderAPIActionBase):
    def certify(self):
        response = self.client.account.certify_beneficial_owner()
        if self.get_errors(response):
            raise ProviderAPIException(
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
        }
