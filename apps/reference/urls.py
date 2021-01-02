from django.urls import path

from apps.reference.views import (CitySearchAPI, CountriesAPI, GetZipCodeAPI,
                                  RegionStateAPI)

urlpatterns = [
    path(
        "countries",
        CountriesAPI.as_view(),
    ),
    path(
        "cities/search",
        CitySearchAPI.as_view(),
    ),
    path(
        "regions",
        RegionStateAPI.as_view(),
    ),
    path(
        "zip_code",
        GetZipCodeAPI.as_view(),
    ),
]
