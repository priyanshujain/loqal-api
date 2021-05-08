from django.utils.translation import gettext as _

from api.views import APIAccessLogView, PosStaffAPIView
from apps.merchant.responses import (PosStaffResponse,
                                     ValidatePosStaffAccessTokenResponse)
from apps.merchant.services import (PosStaffLogin, PosStaffLogout,
                                    UpdatePosStaffMember,
                                    ValidatePosStaffAccessToken)


class PosStaffValidateAccessTokenAPI(APIAccessLogView):
    """
    Create new pos staff api
    """

    def post(self, request):
        pos_staff = ValidatePosStaffAccessToken(
            data=self.request_data
        ).handle()
        return self.response(
            ValidatePosStaffAccessTokenResponse(pos_staff).data
        )


class PosStaffLoginAPI(APIAccessLogView):
    """
    Create new pos staff api
    """

    def post(self, request):
        pos_session = PosStaffLogin(
            request=request, data=self.request_data
        ).handle()
        return self.response()


class PosStaffLogoutAPI(APIAccessLogView):
    """
    Create new pos staff api
    """

    def post(self, request):
        PosStaffLogout(request=request).handle()
        return self.response()


class GetPosStaffProfileAPI(PosStaffAPIView):
    """"""

    def get(self, request):
        pos_staff = request.pos_staff
        return self.response(PosStaffResponse(pos_staff).data)


class UpdatePosStaffProfileAPI(PosStaffAPIView):
    """"""

    def put(self, request):
        UpdatePosStaffMember(
            merchant=request.merchant_account,
            pos_staff=request.pos_staff,
            data=self.request_data,
        ).handle()
        return self.response(status=204)
