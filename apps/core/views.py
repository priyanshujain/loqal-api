from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

from api.helpers import run_validator
from api.views import APIAccessLogView, StaffAPIView
from apps.core.dbapi import (create_app_metadata, create_merchant_metadata,
                             get_app_metadata, get_merchant_metadata,
                             get_platform_app_metadata,
                             get_platform_merchant_metadata,
                             update_app_metadata, update_merchant_metadata)
from apps.core.responses import AppMetaDataResponse, MerchantMetaDataResponse
from apps.core.validators import (AppMetaDataValidator,
                                  MerchantMetaDataValidator)


class AppMetaDataAPI(StaffAPIView):
    def post(self, request):
        data = run_validator(AppMetaDataValidator, self.request_data)
        plaform = get_platform_app_metadata(platform=data["platform"])
        if plaform:
            update_app_metadata(**data)
        else:
            create_app_metadata(**data)
        return self.response()

    def get(self, request):
        platforms = get_app_metadata()
        return self.response(AppMetaDataResponse(platforms, many=True).data)


class MerchantMetaDataAPI(StaffAPIView):
    def post(self, request):
        data = run_validator(MerchantMetaDataValidator, self.request_data)
        plaform = get_platform_merchant_metadata(platform=data["platform"])
        if plaform:
            update_merchant_metadata(**data)
        else:
            create_merchant_metadata(**data)
        return self.response()

    def get(self, request):
        platforms = get_merchant_metadata()
        return self.response(
            MerchantMetaDataResponse(platforms, many=True).data
        )


class GetAppMetaDataAPI(APIAccessLogView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        platforms = get_app_metadata()
        return self.response(AppMetaDataResponse(platforms, many=True).data)


class GetMerchantMetaDataAPI(APIAccessLogView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        platforms = get_merchant_metadata()
        return self.response(
            MerchantMetaDataResponse(platforms, many=True).data
        )
