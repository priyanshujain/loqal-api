from django.utils import datastructures

from api.views import MerchantAPIView
from apps.account.permissions import IsMerchantAccountPendingPermission
from apps.account.responses.merchant import MerchantAccountStatusResponse
from apps.merchant.options import BusinessDocumentType, IndividualDocumentType
from apps.merchant.responses import (ControllerVerificationDocumentResponse,
                                     IncorporationVerificationDocumentResponse,
                                     OnboardingDataResponse,
                                     OnboardingStatusResponse,
                                     OwnerVerificationDocumentResponse)
from apps.merchant.services import (BeneficialOwnerDocumentUpload,
                                    BusinessDocumentUpload,
                                    CertifyDwollaMerchantAccount,
                                    ControllerDocumentUpload,
                                    CreateBeneficialOwner,
                                    CreateControllerDetails,
                                    CreateDwollaMerchantAccount,
                                    CreateIncorporationDetails,
                                    DocumentRequirements,
                                    GetMerchantAccountStatus,
                                    RemoveBeneficialOwner, SubmitDocuments,
                                    UpdateBeneficialOwner,
                                    UpdateControllerDetails,
                                    UpdateIncorporationDetails)

__all__ = (
    "CreateIncorporationDetailsAPI",
    "UpdateIncorporationDetailsAPI",
    "CreateControllerAPI",
    "UpdateControllerAPI",
    "CreateBeneficialOwnerAPI",
    "UpdateBeneficialOwnerAPI",
    "RemoveBeneficialOwnerAPI",
    "OnboardingDataAPI",
    "DocumentRequirementsAPI",
    "UpdateBusinessVerificationDocumentAPI",
    "UpdateOwnerVerificationDocumentAPI",
    "UpdateControllerVerificationDocumentAPI",
    "AcceptableDocumentTypesAPI",
)


class CreateIncorporationDetailsAPI(MerchantAPIView):
    """
    add business entity's incorporation related data as part of the first step for
    merchant onboarding process.
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def post(self, request):
        merchant_account = request.merchant_account
        data = self.request_data
        incorporation_details = CreateIncorporationDetails(
            merchant=merchant_account, data=data
        ).handle()
        return self.response({"id": incorporation_details.id}, status=201)


class UpdateIncorporationDetailsAPI(MerchantAPIView):
    """
    changes to incorporation related data API
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def put(self, request):
        merchant_account = request.merchant_account
        data = self.request_data
        UpdateIncorporationDetails(
            merchant=merchant_account, data=data
        ).handle()
        return self.response(status=204)


class CreateControllerAPI(MerchantAPIView):
    """
    Create merchant account controller data API
    A controller is any natural individual who holds significant
    responsibilities to control, manage, or direct a company or other
    corporate entity (i.e. CEO, CFO, General Partner, President, etc).
    A company may have more than one controller, but only one
    controller’s information must be collected. A controller may be a
    non-US person.
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def post(self, request):
        merchant_id = request.merchant_account.id
        data = self.request_data
        controller_details = CreateControllerDetails(
            merchant_id=merchant_id, data=data
        ).handle()
        return self.response({"id": controller_details.id}, status=201)


class UpdateControllerAPI(MerchantAPIView):
    """
    changes to controller data API
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def put(self, request):
        merchant_id = request.merchant_account.id
        data = self.request_data
        UpdateControllerDetails(merchant_id=merchant_id, data=data).handle()
        return self.response(status=204)


class CreateBeneficialOwnerAPI(MerchantAPIView):
    """
    Add an owner's data API
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def post(self, request):
        merchant_id = request.merchant_account.id
        data = self.request_data
        beneficial_owner = CreateBeneficialOwner(
            merchant_id=merchant_id, data=data
        ).handle()
        return self.response(
            {
                "id": beneficial_owner.id,
                "status": {
                    "label": beneficial_owner.status.label,
                    "value": beneficial_owner.status.value,
                },
            },
            status=201,
        )


class UpdateBeneficialOwnerAPI(MerchantAPIView):
    """
    changes to beneficial owner data API
    """

    def put(self, request):
        merchant_id = request.merchant_account.id
        data = self.request_data
        beneficial_owner = UpdateBeneficialOwner(
            merchant_id=merchant_id, data=data
        ).handle()
        return self.response(
            {
                "id": beneficial_owner.id,
                "status": {
                    "label": beneficial_owner.status.label,
                    "value": beneficial_owner.status.value,
                },
            }
        )


class RemoveBeneficialOwnerAPI(MerchantAPIView):
    """
    remove beneficial owner API
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def delete(self, request):
        merchant_id = request.merchant_account.id
        data = self.request_data
        RemoveBeneficialOwner(merchant_id=merchant_id, data=data).handle()
        return self.response(status=204)


class OnboardingDataAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        data = OnboardingDataResponse(merchant_account).data
        return self.response(data)


class OnboardingStatusAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        account = GetMerchantAccountStatus(merchant=merchant_account).handle()
        return self.response(OnboardingStatusResponse(account).data)


class SubmitKycDataAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        user = request.user
        ip_address = request.ip
        updated_merchant_account = CreateDwollaMerchantAccount(
            merchant_id=merchant_account.id,
            user_id=user.id,
            ip_address=ip_address,
        ).handle()
        return self.response(
            MerchantAccountStatusResponse(updated_merchant_account).data
        )


class DocumentRequirementsAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        required_docs = DocumentRequirements(
            merchant=merchant_account
        ).handle()
        return self.response(required_docs)


class UpdateBusinessVerificationDocumentAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        document = BusinessDocumentUpload(
            merchant=merchant_account, data=self.request_data
        ).handle()
        return self.response(
            IncorporationVerificationDocumentResponse(document).data
        )


class UpdateControllerVerificationDocumentAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        document = ControllerDocumentUpload(
            merchant=merchant_account, data=self.request_data
        ).handle()
        return self.response(
            ControllerVerificationDocumentResponse(document).data
        )


class UpdateOwnerVerificationDocumentAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        document = BeneficialOwnerDocumentUpload(
            merchant=merchant_account, data=self.request_data
        ).handle()
        return self.response(OwnerVerificationDocumentResponse(document).data)


class SubmitDocumentAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        SubmitDocuments(merchant=merchant_account).handle()
        return self.response()


class CertifyOwnershipAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        CertifyDwollaMerchantAccount(merchant=merchant_account).handle()
        return self.response()


class AcceptableDocumentTypesAPI(MerchantAPIView):
    def get(self, request):
        individual_document_types = [
            {"document_type_label": v, "document_type_value": k}
            for k, v in IndividualDocumentType.choices
            if IndividualDocumentType.NOT_APPLICABLE.value != k
        ]
        business_document_types = [
            {"document_type_label": v, "document_type_value": k}
            for k, v in BusinessDocumentType.choices
            if BusinessDocumentType.NOT_APPLICABLE.value != k
        ]

        return self.response(
            {
                "incorporation": business_document_types,
                "controller": individual_document_types,
                "beneficial_owners": individual_document_types,
            }
        )
