from api.exceptions import ValidationError, ErrorDetail
from django.utils.translation import gettext as _

from api.views import APIView
from apps.reference.dbapi import get_all_countries, get_zipcode
from apps.reference.services import (CitySearch,
                                     RegionStateList)
from apps.reference.responses import ZipCodeResponse


class CountriesAPI(APIView):
    def get(self, request):
        countries = [
            {"name": country.name, "iso_code": country.iso_code}
            for country in get_all_countries()
        ]
        return self.response({"countries": countries})


class CitySearchAPI(APIView):
    def get(self, request):
        data = self.request_data
        cities = self._run_services(data=data)
        return self.response({"cities": cities})

    def _run_services(self, data):
        service = CitySearch(data=data)
        return service.handle()


class RegionStateAPI(APIView):
    def get(self, request):
        data = self.request_data
        regions = self._run_services(data=data)
        return self.response({"regions": regions})

    def _run_services(self, data):
        service = RegionStateList(data=data)
        return service.handle()


class GetZipCodeAPI(APIView):
    def get(self, request):
        code = self.request_data.get("code", None)
        if not code:
            raise ValidationError({
                "detail": ErrorDetail(_("code is required."))
            })
        
        zip_code = get_zipcode(code=code)
        if not zip_code:
            raise ValidationError({
                "detail": ErrorDetail(_("code is invalid."))
            })
            
        return self.response(ZipCodeResponse(zip_code).data)
