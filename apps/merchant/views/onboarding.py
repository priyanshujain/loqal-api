from api.views import MerchantAPIView
from apps.account.permissions import IsMerchantAccountPendingPermission
from apps.account.responses.merchant import MerchantAccountProfileResponse
from apps.merchant.responses import OnboardingDataResponse
from apps.merchant.services import (BeneficialOwnerDocumentUpload,
                                    BusinessDocumentUpload,
                                    ControllerDocumentUpload,
                                    CreateBeneficialOwner,
                                    CreateControllerDetails,
                                    CreateDwollaMerchantAccount,
                                    CreateIncorporationDetails,
                                    DocumentRequirements,
                                    RemoveBeneficialOwner,
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
)


class CreateIncorporationDetailsAPI(MerchantAPIView):
    """
    add business entity's incorporation related data as part of the first step for
    merchant onboarding process.
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def post(self, request):
        merchant_id = request.merchant_account.id
        data = self.request_data
        incorporation_details = CreateIncorporationDetails(
            merchant_id=merchant_id, data=data
        ).handle()
        return self.response({"id": incorporation_details.id}, status=201)


class UpdateIncorporationDetailsAPI(MerchantAPIView):
    """
    changes to incorporation related data API
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def put(self, request):
        merchant_id = request.merchant_account.id
        data = self.request_data
        UpdateIncorporationDetails(merchant_id=merchant_id, data=data).handle()
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
        return self.response({"id": beneficial_owner.id}, status=201)


class UpdateBeneficialOwnerAPI(MerchantAPIView):
    """
    changes to beneficial owner data API
    """

    permission_classes = (IsMerchantAccountPendingPermission,)

    def put(self, request):
        merchant_id = request.merchant_account.id
        data = self.request_data
        UpdateBeneficialOwner(merchant_id=merchant_id, data=data).handle()
        return self.response(status=204)


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
    # permission_classes = (IsMerchantAccountPendingPermission,)

    def get(self, request):
        merchant_account = request.merchant_account
        data = OnboardingDataResponse(merchant_account).data
        return self.response(data)


class SubmitKycDataAPI(MerchantAPIView):
    # permission_classes = (IsMerchantAccountPendingPermission,)

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
            MerchantAccountProfileResponse(updated_merchant_account).data
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
        BusinessDocumentUpload(
            merchant=merchant_account, data=self.request_data
        ).handle()
        return self.response()


class UpdateControllerVerificationDocumentAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        ControllerDocumentUpload(
            merchant=merchant_account, data=self.request_data
        ).handle()
        return self.response()


class UpdateOwnerVerificationDocumentAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        BeneficialOwnerDocumentUpload(
            merchant=merchant_account, data=self.request_data
        ).handle()
        return self.response()
