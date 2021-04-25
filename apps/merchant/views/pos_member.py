from django.utils.translation import gettext as _

from api.views import APIAccessLogView
from apps.merchant.dbapi import get_merchant_pos_staff
from apps.merchant.responses import CreatePosStaffResponse, ListPosStaffResponse
from apps.merchant.services import ValidatePosStaffAccessToken


class PosStaffLoginAPI(APIAccessLogView):
    """
    Create new pos staff api
    """

    def post(self, request):
        is_valid = ValidatePosStaffAccessToken(data=self.request_data).handle()
        return self.response({"is_valid": is_valid})
