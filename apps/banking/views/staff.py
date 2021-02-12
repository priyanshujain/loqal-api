from api.views import StaffAPIView


class SyncBankAccountAPI(StaffAPIView):
    def post(self, request, account_id):
        return self.response()


