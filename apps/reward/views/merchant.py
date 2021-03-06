from rest_framework.settings import import_from_string

from api.views import MerchantAPIView
from apps.reward.dbapi import (get_all_loyalty_program,
                               get_current_loyalty_program)
from apps.reward.responses import LoyaltyProgramResponse
from apps.reward.services import (CreateLoyaltyProgram,
                                  DeactivateLoyaltyProgram, EditLoyaltyProgram)


class CreateLoyaltyProgramAPI(MerchantAPIView):
    def post(self, request):
        program = CreateLoyaltyProgram(
            merchant=request.merchant_account, data=self.request_data
        ).handle()
        return self.response(LoyaltyProgramResponse(program).data)


class DeactivateLoyaltyProgramAPI(MerchantAPIView):
    def post(self, request):
        DeactivateLoyaltyProgram(merchant=request.merchant_account).handle()
        return self.response(status=204)


class GetAllLoyaltyProgramAPI(MerchantAPIView):
    def get(self, request):
        programs = get_all_loyalty_program(
            merchant_id=request.merchant_account.id
        )
        return self.response(LoyaltyProgramResponse(programs, many=True).data)


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
