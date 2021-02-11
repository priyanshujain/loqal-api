from django.urls import path

from apps.merchant.views.onboarding import (
    AcceptableDocumentTypesAPI, CertifyOwnershipAPI, CreateBeneficialOwnerAPI,
    CreateControllerAPI, CreateIncorporationDetailsAPI,
    DocumentRequirementsAPI, ForceCertifyOwnershipAPI, OnboardingDataAPI,
    OnboardingStatusAPI, RemoveBeneficialOwnerAPI, SubmitDocumentAPI,
    SubmitKycDataAPI, UpdateBeneficialOwnerAPI,
    UpdateBusinessVerificationDocumentAPI, UpdateControllerAPI,
    UpdateControllerVerificationDocumentAPI, UpdateIncorporationDetailsAPI,
    UpdateOwnerVerificationDocumentAPI)

urlpatterns = [
    path(
        "onboarding/incorporation-details/create/",
        CreateIncorporationDetailsAPI.as_view(),
        name="create_incorporation_details",
    ),
    path(
        "onboarding/incorporation-details/update/",
        UpdateIncorporationDetailsAPI.as_view(),
        name="update_incorporation_details",
    ),
    path(
        "onboarding/controller/create/",
        CreateControllerAPI.as_view(),
        name="create_controller",
    ),
    path(
        "onboarding/controller/update/",
        UpdateControllerAPI.as_view(),
        name="update_controller",
    ),
    path(
        "onboarding/beneficial-owner/create/",
        CreateBeneficialOwnerAPI.as_view(),
        name="create_beneficial_owner",
    ),
    path(
        "onboarding/beneficial-owner/update/",
        UpdateBeneficialOwnerAPI.as_view(),
        name="update_beneficial_owner",
    ),
    path(
        "onboarding/beneficial-owner/remove/",
        RemoveBeneficialOwnerAPI.as_view(),
        name="remove_beneficial_owner",
    ),
    path(
        "onboarding/data/",
        OnboardingDataAPI.as_view(),
        name="view_onboarding_data",
    ),
    path(
        "onboarding/status/",
        OnboardingStatusAPI.as_view(),
        name="view_onboarding_status",
    ),
    path(
        "onboarding/submit-kyc/",
        SubmitKycDataAPI.as_view(),
        name="submit_kyc_data",
    ),
    path(
        "onboarding/required-documents/",
        DocumentRequirementsAPI.as_view(),
        name="required_documents",
    ),
    path(
        "onboarding/incorporation-details/document-upload/",
        UpdateBusinessVerificationDocumentAPI.as_view(),
        name="incorporation_document_upload",
    ),
    path(
        "onboarding/controller/document-upload/",
        UpdateControllerVerificationDocumentAPI.as_view(),
        name="controller_document_upload",
    ),
    path(
        "onboarding/beneficial-owner/document-upload/",
        UpdateOwnerVerificationDocumentAPI.as_view(),
        name="beneficial_owner_document_upload",
    ),
    path(
        "onboarding/submit-documents/",
        SubmitDocumentAPI.as_view(),
        name="submit_documents",
    ),
    path(
        "onboarding/certify-ownership/",
        CertifyOwnershipAPI.as_view(),
        name="certify_ownership",
    ),
    path(
        "onboarding/force-certify-ownership/",
        ForceCertifyOwnershipAPI.as_view(),
        name="force_certify_ownership",
    ),
    path(
        "onboarding/acceptable-document-types/",
        AcceptableDocumentTypesAPI.as_view(),
        name="acceptable_document_types",
    ),
]
