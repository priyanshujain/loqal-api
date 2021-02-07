from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import StaffAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.merchant.dbapi import (get_merchant_code_protocols,
                                 get_merchant_operation_hours,
                                 get_merchant_service_availability)
from apps.merchant.dbapi.non_loqal import delete_non_loqal
from apps.merchant.responses import (CodesAndProtocolsResponse,
                                     MerchantOperationHoursResponse,
                                     MerchantProfileResponse,
                                     ServiceAvailabilityResponse)
from apps.merchant.services import (UpdateCodesAndProtocols,
                                    UpdateMerchantProfile,
                                    UpdateOperationHours,
                                    UpdateServiceAvailability)

__all__ = (
    "UpdateMerchantProfileAPI",
    "GetMerchantProfileAPI",
    "UpdateMerchantOperationHoursAPI",
    "GetMerchantOperationHoursAPI",
    "UpdateCodesAndProtocolsAPI",
    "GetCodesAndProtocolsAPI",
    "GetServiceAvailabilityAPI",
    "UpdateServiceAvailabilityAPI",
    "DeleteNonLoqalAPI",
)


class StaffBaseMerchantAPI(StaffAPIView):
    def validate_merchant(self, merchant_id):
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_id
        )
        if not merchant_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        return merchant_account


class UpdateMerchantProfileAPI(StaffBaseMerchantAPI):
    def put(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        # TODO: 1. create a separate API for updating hero image
        UpdateMerchantProfile(
            merchant=merchant_account, data=self.request_data
        ).handle()
        return self.response(status=204)


class GetMerchantProfileAPI(StaffBaseMerchantAPI):
    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        try:
            merchant_profile = merchant_account.profile
        except AttributeError:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant profile."))}
            )
        return self.response(MerchantProfileResponse(merchant_profile).data)


class UpdateMerchantOperationHoursAPI(StaffBaseMerchantAPI):
    def put(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        UpdateOperationHours(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=204)


class GetMerchantOperationHoursAPI(StaffBaseMerchantAPI):
    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        operation_hours = get_merchant_operation_hours(
            merchant_id=merchant_account.id
        )
        if not operation_hours:
            return self.response()
        return self.response(
            MerchantOperationHoursResponse(operation_hours, many=True).data
        )


class UpdateCodesAndProtocolsAPI(StaffBaseMerchantAPI):
    def put(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        UpdateCodesAndProtocols(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=204)


class GetCodesAndProtocolsAPI(StaffBaseMerchantAPI):
    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        code_protocols = get_merchant_code_protocols(
            merchant_id=merchant_account.id
        )
        if not code_protocols:
            return self.response()
        return self.response(CodesAndProtocolsResponse(code_protocols).data)


class GetServiceAvailabilityAPI(StaffBaseMerchantAPI):
    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        service_availability = get_merchant_service_availability(
            merchant_id=merchant_account.id
        )
        if not service_availability:
            return self.response()
        return self.response(
            ServiceAvailabilityResponse(service_availability).data
        )


class UpdateServiceAvailabilityAPI(StaffBaseMerchantAPI):
    def put(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        UpdateServiceAvailability(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=204)


class DeleteNonLoqalAPI(StaffBaseMerchantAPI):
    def delete(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        if merchant_account.account:
            raise ValidationError(
                {"detail": ErrorDetail(_("This is not non loqal merchant"))}
            )
        delete_non_loqal(merchant_id=merchant_account.id)
        return self.response(status=204)
