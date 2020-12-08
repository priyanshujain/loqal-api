"""
Handled exceptions raised by Dwolla APIs.
"""

# TODO: update error module using
# https://github.com/Dwolla/dwolla-v2-python/blob/d9c529eda2c9e9829ccde4bdbacbcdd41d1b074b/dwollav2/error.py

import json

import yaml

from api.exceptions import APIException

__all__ = "ApiError"


class ApiError(APIException):
    def __init__(self, verb, route, params, response):
        super(ApiError, self).__init__()
        self.verb = verb
        self.route = route
        self.params = params

        self.raw_response = response
        self.status_code = None if response is None else response.status_code

        self.code = None
        self.messages = []
        self.errors = {}

        if response is not None:
            try:
                self.errors = response.json()
            except json.decoder.JSONDecodeError:
                self.errors = response.content

    def __str__(self):
        class_name = self.__class__.__name__

        error_details = {
            "request": {
                "parameters": self.params,
                "verb": str(self.verb),
                "url": self.route,
            },
            "response": {
                "status_code": self.status_code,
            },
            "errors": self.errors,
        }

        return "{class_name}\n{separator}\n{dump}\n".format(
            class_name=class_name,
            separator="---",
            dump=yaml.safe_dump(error_details, default_flow_style=False),
        )


class BadRequestError(ApiError):
    pass


class AuthenticationError(ApiError):
    pass


class ForbiddenError(ApiError):
    pass


class TooManyRequestsError(ApiError):
    pass


class InternalApplicationError(ApiError):
    pass


class NotFoundError(ApiError):
    pass
