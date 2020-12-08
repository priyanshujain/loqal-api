import yaml

from api.exceptions import APIException

__all__ = (
    "APIException",
    "IntegrationAPIError",
    "InvalidRequestError",
    "InvalidInputError",
)


class IntegrationAPIError(APIException):
    def __init__(self, errors):
        super().__init__()

        self.errors = errors

    def __str__(self):
        class_name = self.__class__.__name__

        error_details = {
            "errors": self.errors,
        }

        return "{class_name}\n{separator}\n{dump}\n".format(
            class_name=str(class_name),
            separator="---",
            dump=yaml.safe_dump(error_details, default_flow_style=False),
        )


class InvalidRequestError(IntegrationAPIError):
    """The request is malformed and cannot be processed."""

    pass


class InvalidInputError(IntegrationAPIError):
    """The request is correctly formatted, but the values are incorrect."""

    pass


class ServerError(IntegrationAPIError):
    """Planned maintenance or an API internal server error."""

    pass
