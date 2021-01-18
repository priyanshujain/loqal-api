from django.utils.translation import gettext as _

from api.views import LoggedInAPIView
from apps.notification.responses import RegisterUserDeviceResponse
from apps.notification.services import (SubscribePushNotication,
                                        UnSubscribePushNotication)


class SubscribePushNoticationAPI(LoggedInAPIView):
    def post(self, request):
        user_device = SubscribePushNotication(
            request=request,
            data=self.request_data,
        ).handle()
        return self.response(RegisterUserDeviceResponse(user_device).data)


class UnSubscribePushNoticationAPI(LoggedInAPIView):
    def post(self, request):
        user_device = UnSubscribePushNotication(
            request=request,
            data=self.request_data,
        ).handle()
        return self.response()
