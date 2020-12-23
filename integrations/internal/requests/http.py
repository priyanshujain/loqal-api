from urllib.parse import urljoin

from requests import Request

__all__ = ("HttpRequest",)


class HttpRequest(object):
    ALLOWED_METHODS = ["POST", "GET"]
    DEFAULT_TIMEOUT = 600  # 10 minutes

    def __init__(self, request_tracker):
        self.request_tracker = request_tracker

    def get_request(
        self, origin, endpoint, session, params, headers, is_json=True
    ):
        return self._http_request(
            origin=origin,
            endpoint=endpoint,
            session=session,
            method="GET",
            params=params,
            headers=headers,
            timeout=self.DEFAULT_TIMEOUT,
            is_json=is_json,
        )

    def post_request(
        self, origin, endpoint, session, headers, data, files, is_json=True
    ):
        return self._http_request(
            origin=origin,
            endpoint=endpoint,
            session=session,
            method="POST",
            data=data,
            files=files,
            headers=headers,
            timeout=self.DEFAULT_TIMEOUT,
            is_json=is_json,
        )

    def _http_request(
        self,
        origin,
        endpoint,
        session,
        method,
        params=None,
        data=None,
        files=None,
        headers=None,
        timeout=None,
        is_json=True,
    ):
        if not session:
            raise ValueError("Invalid session")

        url = self.__build_url(origin, endpoint)

        if self.request_tracker:
            self.request_tracker.start_new_request(
                origin=origin,
                endpoint=endpoint,
                query_params=params or {},
                headers=headers,
                method=method,
                data=data or {},
                files=files,
            )

        prepared_request = self._requests_http_request(
            url, session, method, params, data or {}, files, headers or {}
        )
        send_kwargs = {
            "timeout": timeout or self.DEFAULT_TIMEOUT,
        }
        response = session.send(prepared_request, **send_kwargs)
        if self.request_tracker:
            self.request_tracker.add_response(
                request_time_taken=response.elapsed.total_seconds(),
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
            )

        return response

    def _requests_http_request(
        self, url, session, method, params, data, files, headers
    ):
        normalized_method = method.upper()
        if normalized_method in self.ALLOWED_METHODS:
            req = Request(
                method=normalized_method,
                url=url,
                headers=headers,
                params=params or {},
                files=files,
                data=data or {},
            )
            prep = session.prepare_request(req)
        else:
            raise ValueError("Invalid request method {}".format(method))
        return prep

    def __build_url(self, origin, endpoint):
        # FIX: Use urljoin to join the url
        return urljoin(origin, endpoint)
