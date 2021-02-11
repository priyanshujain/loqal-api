"""
This module provides a Mixin to generate http requests to the CC API endpoints.
"""

import json

from integrations.dwolla.errors import *
from integrations.internal.requests import HttpRequest

__all__ = "Http"


class Http(HttpRequest):
    """
    Mixin for other Client classes. Provides abstract get/post methods that will add authentication
    headers when necessary and poin to the appropriate host for the environment.
    """

    def __init__(self, config):
        self.config = config
        self.session = config.session
        super().__init__(request_tracker=config.request_tracker)

    def get(
        self,
        endpoint,
        query=None,
        authenticated=True,
        api_type="api",
        version="v1",
        retry=False,
    ):
        """Executes a GET request."""

        origin = self.__environment_url(api_type, version)
        headers = self.__build_headers(
            authenticated=authenticated, method="get", api_type=api_type
        )

        def execute_request(headers):
            return self.get_request(
                origin=origin,
                endpoint=endpoint,
                session=self.session,
                headers=headers,
                params=query,
            )

        url = self.__build_url(endpoint, api_type, version)
        response = self.__handle_authentication_errors(
            method="get",
            execute_request=execute_request,
            retry=retry,
            headers=headers,
            api_type=api_type,
            authenticated=authenticated,
        )

        return self.__handle_errors("get", url, query, response)

    # TODO: reduce functional parameters to this function
    # FIX: https://softwareengineering.stackexchange.com/questions/145055/are-there-guidelines-on-how-many-parameters-a-function-should-accept
    def post(
        self,
        endpoint,
        data={},
        custom_content_type="application/json",
        files=None,
        authenticated=True,
        api_type="api",
        version="v1",
        retry=False,
    ):
        """Executes a POST request."""

        url = self.__build_url(endpoint, api_type, version)
        headers = self.__build_headers(
            authenticated=authenticated,
            method="post",
            api_type=api_type,
            custom_content_type=custom_content_type,
        )
        data = self.__build_data(custom_content_type, data)
        origin = self.__environment_url(api_type, version)

        def execute_request(headers):
            return self.post_request(
                origin=origin,
                endpoint=endpoint,
                session=self.session,
                headers=headers,
                data=data,
                files=files,
            )

        response = self.__handle_authentication_errors(
            method="post",
            execute_request=execute_request,
            retry=retry,
            headers=headers,
            api_type=api_type,
            authenticated=authenticated,
        )

        return self.__handle_errors("post", url, data, response)

    def __build_url(self, endpoint, api_type, version):
        return self.__environment_url(api_type, version) + endpoint

    def __build_data(self, custom_content_type, data):
        if custom_content_type == "application/json":
            if data:
                data = json.dumps(data)
            return data
        else:
            return data

    def __environment_url(self, api_type, version):
        return self.config.environment_url(api_type, version)

    def __build_headers(
        self,
        authenticated,
        method="get",
        api_type="api",
        custom_content_type=None,
    ):
        headers = {}

        if api_type == "api":
            headers["Accept"] = "application/vnd.dwolla.v1.hal+json"

        if method == "post":
            headers["Content-Type"] = "application/vnd.dwolla.v1.hal+json"

        if custom_content_type:
            headers["Content-Type"] = custom_content_type

        # TODO: Fix this
        if custom_content_type == "multipart/form-data":
            del headers["Content-Type"]

        if authenticated:
            headers["Authorization"] = f"Bearer {self.config.auth_token}"

        return headers

    HTTP_CODE_TO_ERROR = {
        400: BadRequestError,
        401: AuthenticationError,
        403: ForbiddenError,
        404: NotFoundError,
        429: TooManyRequestsError,
        500: InternalApplicationError,
    }

    def __handle_errors(self, verb, url, params, response):
        if int(response.status_code / 100) == 2:
            return response
        else:
            klass = Http.HTTP_CODE_TO_ERROR.get(response.status_code, ApiError)
            raise klass(verb, url, params, response)

    def __handle_authentication_errors(
        self, method, execute_request, retry, headers, api_type, authenticated
    ):
        retry_count = 3 if retry else 2

        while retry_count:
            retry_count -= 1
            response = execute_request(headers)
            if response.status_code != 401:
                return response

            if retry_count:
                self.config.reauthenticate()
                headers = self.__build_headers(
                    authenticated=authenticated,
                    method=method,
                    api_type=api_type,
                )
        return response
