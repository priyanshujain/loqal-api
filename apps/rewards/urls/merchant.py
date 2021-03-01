from django.urls import path

from apps.rewards.views.merchant import (CreateLoyaltyProgramAPI,
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
        "merchant/loyalty-program/",
        GetLoyaltyProgramAPI.as_view(),
        name="get_loyalty_program",
    ),
]
