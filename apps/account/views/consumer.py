from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import APIView, ConsumerAPIView, ConsumerPre2FaAPIView
from apps.account.responses import ConsumerAccountProfileResponse
from apps.account.services import (AddZipCode, ChangeAccountUsername,
                                   CheckAccountUsername, CreateConsumerAccount)
from apps.account.services.accept_consumer_terms import AcceptTerms
from apps.user.services import AfterLogin
from utils.auth import login

__all__ = (
    "ConsumerSignupAPI",
    "AddAccountZipCodeAPI",
    "ConsumerAccountProfileAPI",
    "AcceptTermsDocumentAPI",
)


class ConsumerSignupAPI(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            raise ValidationError(
                {"detail": ErrorDetail(_("User has aleady logged in."))}
            )

        self._run_services(ip_address=request.ip)
        return self.response(status=201)

    def _run_services(self, ip_address):
        data = self.request_data
        service = CreateConsumerAccount(
            request=self.request, data=self.request_data
        )
        consumer_account = service.handle()
        user = consumer_account.user
        login(request=self.request, user=user)
        AfterLogin(request=self.request, user=user, send_alert=False).handle()


class AddAccountZipCodeAPI(ConsumerAPIView):
    def post(self, request):
        account = request.account
        self._run_services(account=account)
        return self.response()

    def _run_services(self, account):
        data = self.request_data
        service = AddZipCode(data=self.request_data, account=account)
        service.handle()


class ConsumerAccountProfileAPI(ConsumerPre2FaAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        return self.response(
            ConsumerAccountProfileResponse(consumer_account).data
        )


class ChangeAccountUsernameAPI(ConsumerAPIView):
    def post(self, request):
        consumer_account = request.consumer_account
        return self.response(
            ChangeAccountUsername(
                consumer_account=consumer_account, data=self.request_data
            ).handle()
        )


class CheckAccountUsernameAPI(ConsumerAPIView):
    def post(self, request):
        consumer_account = request.consumer_account
        return self.response(
            CheckAccountUsername(
                consumer_account=consumer_account, data=self.request_data
            ).handle()
        )


class AcceptTermsDocumentAPI(ConsumerPre2FaAPIView):
    def post(self, request):
        AcceptTerms(
            request=request,
            account=request.account,
            user=request.user,
            data=self.request_data,
        ).handle()
        return self.response()
