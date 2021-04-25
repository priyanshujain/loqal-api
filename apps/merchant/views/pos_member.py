from django.utils.translation import gettext as _

from api.views import APIAccessLogView
from apps.merchant.services import PosStaffLogin, ValidatePosStaffAccessToken


class PosStaffValidateAccessTokenAPI(APIAccessLogView):
    """
    Create new pos staff api
    """

    def post(self, request):
        is_valid = ValidatePosStaffAccessToken(data=self.request_data).handle()
        return self.response({"is_valid": is_valid})


class PosStaffLoginAPI(APIAccessLogView):
    """
    Create new pos staff api
    """

    def post(self, request):
        pos_session = PosStaffLogin(
            request=request, data=self.request_data
        ).handle()
        return self.response()
