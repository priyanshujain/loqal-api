from apps.tracking.models import (APIAccessLog, PspApiRequestStorage,
                                  RawPspApiRequest, RawPspApiResponse)


def create_api_access_log(**args):
    return APIAccessLog.objects.create(**args)


def create_psp_api_request(account_id, psp_id, request_id):
    try:
        return PspApiRequestStorage.objects.create(
            account_id=account_id, psp_id=psp_id, request_id=request_id
        )
    except PspApiRequestStorage.DoesNotExist:
        return None


def create_raw_api_request(
    origin, endpoint, query_params, headers, method, data, files
):
    """
    TODO: find a way to store files data for raw request
    """
    try:
        return RawPspApiRequest.objects.create(
            origin=origin,
            endpoint=endpoint,
            query_params=query_params or {},
            headers=headers or {},
            method=method,
            data=data or {},
            files=[],
        )
    except RawPspApiRequest.DoesNotExist:
        return None


def create_raw_api_response(request_time_taken, status_code, headers, content):
    try:
        return RawPspApiResponse.objects.create(
            request_time_taken=request_time_taken,
            status_code=status_code,
            headers=headers or {},
            content=content or b"",
        )
    except RawPspApiResponse.DoesNotExist:
        return None


def filter_psp_request_errors(account_id):
    return PspApiRequestStorage.objects.filter(
        account_id=account_id, request__response__isnull=False
    ).filter(request__response__status_code__gte=400)


def all_psp_requests(account_id):
    return PspApiRequestStorage.objects.filter(account_id=account_id)


def get_psp_request(request_id, account_id):
    try:
        return PspApiRequestStorage.objects.get(
            id=request_id, account_id=account_id
        )
    except PspApiRequestStorage.DoesNotExist:
        return None
