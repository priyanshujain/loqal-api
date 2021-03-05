from django.urls import path

from apps.reward.views.merchant import (CreateLoyaltyProgramAPI,
                                         DeactivateLoyaltyProgramAPI,
                                         GetAllLoyaltyProgramAPI,
                                         GetLoyaltyProgramAPI,
                                         UpdateLoyaltyProgramAPI)

urlpatterns = [
    path(
        "merchant/loyalty-program/create/",
        CreateLoyaltyProgramAPI.as_view(),
        name="create_loyalty_program",
    ),
    path(
        "merchant/loyalty-program/update/",
        UpdateLoyaltyProgramAPI.as_view(),
        name="update_loyalty_program",
    ),
    path(
        "merchant/loyalty-program/de-activate/",
        DeactivateLoyaltyProgramAPI.as_view(),
        name="deactivate_loyalty_program",
    ),
    path(
        "merchant/loyalty-program/all/",
        GetAllLoyaltyProgramAPI.as_view(),
        name="all_loyalty_programs",
    ),
    path(
        "merchant/loyalty-program/",
        GetLoyaltyProgramAPI.as_view(),
        name="get_loyalty_program",
    ),
]
