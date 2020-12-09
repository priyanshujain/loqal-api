from api.views import UserAPIView
from apps.account.permissions import IsMerchantAccountPendingPermission
from apps.onboarding.responses import (OnboardingDataResponse,
                                       OnboardingRecordReponse)
from apps.onboarding.services import (CreateAuthorizedSignatory,
                                      CreateCompanyOfficer,
                                      CreateIncorporationDetails,
                                      CreatePaymentAccountUsage,
                                      RemoveCompanyOfficer,
                                      UpdateAuthorisedSignatory,
                                      UpdateCompanyOfficer,
                                      UpdateIncorporationDetails,
                                      UpdatePaymentAccountUsage)


class CreateIncorporationDetailsAPI(UserAPIView):
    permission_classes = (
        IsMerchantAccountPendingPermission,
    )

    def post(self, request):
        data = self.request_data
        account_id = request.account.id

        incorporation_details = self._run_services(account_id, data)
        return self.response({"id": incorporation_details.id}, status=201)

    def _run_services(self, account_id, data):
        service = CreateIncorporationDetails(account_id, data)
        return service.execute()


class UpdateIncorporationDetailsAPI(UserAPIView):
    permission_classes = (
        IsMerchantAccountPendingPermission,
    )

    def put(self, request):
        data = self.request_data
        account_id = request.account.id
        self._run_services(account_id, data)
        return self.response(status=204)

    def _run_services(self, account_id, data):
        service = UpdateIncorporationDetails(account_id, data)
        return service.execute()


class CreateControllerAPI(UserAPIView):
    permission_classes = (
        IsMerchantAccountPendingPermission,
    )

    def post(self, request):
        data = self.request_data
        account_id = request.account.id

        authorised_signatory = self._run_services(account_id, data)
        return self.response({"id": authorised_signatory.id}, status=201)

    def _run_services(self, account_id, data):
        service = CreateAuthorizedSignatory(account_id, data)
        return service.execute()


class UpdateControllerAPI(UserAPIView):
    permission_classes = (
        IsMerchantAccountPendingPermission,
    )

    def put(self, request):
        data = self.request_data
        account_id = request.account.id

        self._run_services(account_id, data)
        return self.response()

    def _run_services(self, account_id, data):
        service = UpdateAuthorisedSignatory(account_id, data)
        return service.execute()


class CreateCompanyOfficerAPI(UserAPIView):
    permission_classes = (
        IsMerchantAccountPendingPermission,
    )

    def post(self, request):
        data = self.request_data
        account_id = request.account.id

        company_officer = self._run_services(account_id, data)
        return self.response({"id": company_officer.id}, status=201)

    def _run_services(self, account_id, data):
        service = CreateCompanyOfficer(account_id, data)
        return service.execute()


class UpdateCompanyOfficerAPI(UserAPIView):
    permission_classes = (
        IsMerchantAccountPendingPermission,
    )

    def put(self, request):
        data = self.request_data
        account_id = request.account.id

        self._run_services(account_id, data)
        return self.response(status=204)

    def _run_services(self, account_id, data):
        service = UpdateCompanyOfficer(account_id, data)
        return service.execute()


class RemoveCompanyOfficerAPI(UserAPIView):
    permission_classes = (
        IsMerchantAccountPendingPermission,
    )

    def delete(self, request):
        data = self.request_data
        account_id = request.account.id

        self._run_services(account_id, data)
        return self.response(status=204)

    def _run_services(self, account_id, data):
        service = RemoveCompanyOfficer(account_id, data)
        return service.execute()


class OnboardingDataAPI(UserAPIView):
    permission_classes = (
        IsMerchantAccountPendingPermission,
    )

    def get(self, request):
        data = OnboardingDataResponse(request.account).data
        return self.response(data)
