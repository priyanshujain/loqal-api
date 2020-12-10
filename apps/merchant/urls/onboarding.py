from django.urls import path

from apps.merchant.views.onboarding import (
    CreateIncorporationDetailsAPI,
    UpdateIncorporationDetailsAPI,
    CreateControllerAPI,
    UpdateControllerAPI,
    CreateBeneficialOwnerAPI,
    UpdateBeneficialOwnerAPI,
    RemoveBeneficialOwnerAPI,
    OnboardingDataAPI,
)

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
]
