from rest_framework import status
from rest_framework.exceptions import (APIException, AuthenticationFailed,
                                       ErrorDetail, MethodNotAllowed,
                                       NotAcceptable, NotAuthenticated,
                                       NotFound, ParseError, PermissionDenied,
                                       Throttled, UnsupportedMediaType,
                                       ValidationError)

__all__ = (
    "APIException",
    "ResourceDoesNotExist",
    "WhiteAPIException",
    "ProviderAPIException",
    "ValidationError",
    "ErrorDetail",
    "AuthenticationFailed",
    "NotAuthenticated",
    "PermissionDenied",
    "MethodNotAllowed",
    "NotAcceptable",
    "ParseError",
    "UnsupportedMediaType",
    "Throttled",
    "NotFound",
    "InternalDBError",
)


class APIException(APIException):
    """
    Status: HTTP_500_INTERNAL_SERVER_ERROR
    """

    pass


class InternalDBError(APIException):
    """
    Status: HTTP_500_INTERNAL_SERVER_ERROR
    """

    default_detail = "The Object creation failed please try again."


class ResourceDoesNotExist(APIException):
    """
    Exception when resource does not exist.
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "The requested resource does not exist"


class WhiteAPIException(APIException):
    """
    Base Exception for the project
    """

    code = ""
    message = ""

    def __init__(self, code=None, message=None, detail=None, **kwargs):
        # Note that we no longer call the base `__init__` here. This is because
        # DRF now forces all detail messages that subclass `APIException` to a
        # string, which breaks our format.
        # https://www.django-rest-framework.org/community/3.0-announcement/#miscellaneous-notes
        if detail is None:
            detail = {
                "code": code or self.code,
                "message": message or self.message,
                "extra": kwargs,
            }

        self.detail = {"detail": detail}


class ProviderAPIException(APIException):
    """
    Exception when Payment service provider throws exception
    Gives HTTP_500_INTERNAL_SERVER_ERROR
    """

    def __init__(self, detail, **kwargs):
        self.detail = detail


class ValidationError(ValidationError):
    """
    Status: HTTP_400_BAD_REQUEST
    """

    pass


class ErrorDetail(ErrorDetail):
    pass


class AuthenticationFailed(AuthenticationFailed):
    """
    Status: HTTP_401_UNAUTHORIZED
    """

    pass


class NotAuthenticated(NotAuthenticated):
    """
    Status: HTTP_401_UNAUTHORIZED
    """

    pass


class PermissionDenied(PermissionDenied):
    """
    Status: HTTP_403_FORBIDDEN
    """

    pass


class NotFound(NotFound):
    """
    Status: HTTP_404_NOT_FOUND
    """

    pass


class MethodNotAllowed(MethodNotAllowed):
    """
    Status: HTTP_405_METHOD_NOT_ALLOWED
    """

    pass


class NotAcceptable(NotAcceptable):
    """
    Status: HTTP_406_NOT_ACCEPTABLE
    """

    pass


class ParseError(ParseError):
    """
    Status: HTTP_400_BAD_REQUEST
    """

    pass


class UnsupportedMediaType(UnsupportedMediaType):
    """
    Status: HTTP_415_UNSUPPORTED_MEDIA_TYPE
    """

    pass


class Throttled(Throttled):
    """
    Status: HTTP_429_TOO_MANY_REQUESTS
    """

    pass
