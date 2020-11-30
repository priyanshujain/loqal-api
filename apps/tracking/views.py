from api.views import APIView
from apps.tracking.dbapi import (all_psp_requests, filter_psp_request_errors,
                                 get_psp_request)
from apps.tracking.responses import PspRequestAPIResponse


class PspRequestAPIView(APIView):
    def get(self, request, account_id):
        psp_requests = all_psp_requests(account_id=account_id)
        return self.paginate(
            request,
            queryset=psp_requests,
            order_by="-created_at",
            response_serializer=PspRequestAPIResponse,
        )


class PspRequestErrorsAPIView(APIView):
    def get(self, request, account_id):
        psp_requests = filter_psp_request_errors(account_id=account_id)
        return self.paginate(
            request,
            queryset=psp_requests,
            order_by="-created_at",
            response_serializer=PspRequestAPIResponse,
        )


class PspRequestDetailsAPIView(APIView):
    def get(self, request, account_id, request_id):
        psp_request = get_psp_request(
            request_id=request_id, account_id=account_id
        )
        if not psp_request:
            return self.response(status=404)
        return self.response(PspRequestAPIResponse(psp_request).data)
