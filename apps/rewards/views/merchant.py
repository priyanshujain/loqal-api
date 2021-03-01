from rest_framework.settings import import_from_string

from api.views import MerchantAPIView
from apps.rewards.dbapi import get_current_loyalty_program
from apps.rewards.responses import LoyaltyProgramResponse
from apps.rewards.services import CreateLoyaltyProgram, EditLoyaltyProgram


class CreateLoyaltyProgramAPI(MerchantAPIView):
    def post(self, request):
        program = CreateLoyaltyProgram(
            merchant=request.merchant_account, data=self.request_data
        ).handle()
        return self.response(LoyaltyProgramResponse(program).data)


class UpdateLoyaltyProgramAPI(MerchantAPIView):
    def put(self, request):
        EditLoyaltyProgram(
            merchant=request.merchant_account, data=self.request_data
        ).handle()
        return self.response(status=204)


class GetLoyaltyProgramAPI(MerchantAPIView):
    def get(self, request):
        program = get_current_loyalty_program(
            merchant_id=request.merchant_account.id
        )
        if not program:
            return self.response()
        return self.response(LoyaltyProgramResponse(program).data)
