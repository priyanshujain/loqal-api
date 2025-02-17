from django.utils.translation import gettext as _
from rest_framework.parsers import MultiPartParser

from api.exceptions import ErrorDetail, ValidationError
from api.views import MerchantAPIView
from apps.merchant.dbapi import (get_merchant_code_protocols,
                                 get_merchant_operation_hours,
                                 get_merchant_service_availability,
                                 get_store_image)
from apps.merchant.responses import (CodesAndProtocolsResponse,
                                     ListStoreImageResponse,
                                     MerchantOperationHoursResponse,
                                     MerchantProfileResponse,
                                     ServiceAvailabilityResponse,
                                     StoreImageResponse)
from apps.merchant.services import (AddStoreImage, UpdateCodesAndProtocols,
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
    "UploadStoreImageAPI",
    "ListStoreImageAPI",
)


class UpdateMerchantProfileAPI(MerchantAPIView):
    def put(self, request):
        merchant_account = request.merchant_account
        # TODO: 1. create a separate API for updating hero image
        UpdateMerchantProfile(
            merchant=merchant_account, data=self.request_data
        ).handle()
        return self.response(status=204)


class GetMerchantProfileAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        try:
            merchant_profile = merchant_account.profile
        except AttributeError:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant profile."))}
            )
        return self.response(MerchantProfileResponse(merchant_profile).data)


class UpdateMerchantOperationHoursAPI(MerchantAPIView):
    def put(self, request):
        merchant_account = request.merchant_account
        UpdateOperationHours(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=204)


class GetMerchantOperationHoursAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        operation_hours = get_merchant_operation_hours(
            merchant_id=merchant_account.id
        )
        if not operation_hours:
            return self.response()
        return self.response(
            MerchantOperationHoursResponse(operation_hours, many=True).data
        )


class UpdateCodesAndProtocolsAPI(MerchantAPIView):
    def put(self, request):
        merchant_account = request.merchant_account
        UpdateCodesAndProtocols(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=204)


class GetCodesAndProtocolsAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        code_protocols = get_merchant_code_protocols(
            merchant_id=merchant_account.id
        )
        if not code_protocols:
            return self.response()
        return self.response(CodesAndProtocolsResponse(code_protocols).data)


class GetServiceAvailabilityAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        service_availability = get_merchant_service_availability(
            merchant_id=merchant_account.id
        )
        if not service_availability:
            return self.response()
        return self.response(
            ServiceAvailabilityResponse(service_availability).data
        )


class UpdateServiceAvailabilityAPI(MerchantAPIView):
    def put(self, request):
        merchant_account = request.merchant_account
        UpdateServiceAvailability(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=204)


class UploadStoreImageAPI(MerchantAPIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        store_image = AddStoreImage(
            merchant=request.merchant_account, data=request.data
        ).handle()
        return self.response(StoreImageResponse(store_image).data)


class ListStoreImageAPI(MerchantAPIView):
    def get(self, request):
        images = request.merchant_account.images
        return self.response(ListStoreImageResponse(images, many=True).data)


class DeleteStoreImageAPI(MerchantAPIView):
    def delete(self, request, image_id):
        store_image = get_store_image(
            merchant_id=request.merchant_account.id, image_id=image_id
        )
        if not store_image:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Image couldn't be deleted please try again.")
                    ),
                    "message": ErrorDetail(_("Invalid image_id.")),
                }
            )
        store_image.delete()
        return self.response()
