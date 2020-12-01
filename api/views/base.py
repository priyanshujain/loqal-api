import functools
import json
import logging
import re
import time
import traceback

from django.conf import settings
from django.db import connection
from django.utils import timezone
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView as View

from api.exceptions import (APIException, AuthenticationFailed,
                            NotAuthenticated, ParseError, PermissionDenied,
                            UnsupportedMediaType, ValidationError)
from apps.tracking.dbapi import create_api_access_log
from apps.user.dbapi import get_session

logger = logging.getLogger(__name__)


class APIView(View):
    parser_classes = (
        JSONParser,
        MultiPartParser,
        FormParser,
    )
    renderer_classes = (JSONRenderer,)
    skip_request_logging = False

    def __init__(self, **args):
        self.started_at = timezone.now()
        self.request_data = {}
        self.response_count = 0
        super().__init__(**args)

    def initialize_request(self, request, *args, **kwargs):
        """
        # TODO: Fill
        """
        self._update_user_session(request=request)
        self.time_started = time.time()
        if getattr(settings, "SQL_DEBUG", False):
            self.queries_before = len(connection.queries)

        # If there are any custom headers in REMOTE_HOST_HEADERS, make sure
        # they respect the allowed proxy list
        if all(
            [
                settings.PROXY_IP_ALLOWED_LIST,
                request.environ.get("REMOTE_ADDR")
                not in settings.PROXY_IP_ALLOWED_LIST,
                request.environ.get("REMOTE_HOST")
                not in settings.PROXY_IP_ALLOWED_LIST,
            ]
        ):
            for custom_header in settings.REMOTE_HOST_HEADERS:
                if custom_header.startswith("HTTP_"):
                    request.environ.pop(custom_header, None)

        drf_request = super(APIView, self).initialize_request(
            request, *args, **kwargs
        )
        request.drf_request = drf_request

        if request.method in ["GET", "DELETE"]:
            self.request_data = request.GET.dict()
        else:
            self.request_data = drf_request.data

        try:
            request.drf_request_user = getattr(drf_request, "user", False)
        except (
            AuthenticationFailed,
            NotAuthenticated,
            PermissionDenied,
            ParseError,
        ) as exc:
            request.drf_request_user = None
            self.__init_request_error__ = exc
        except UnsupportedMediaType as exc:
            exc.detail = _(
                "You did not use correct Content-Type in your HTTP request. "
                "If you are using our REST API, the Content-Type must be application/json"
            )
            self.__init_request_error__ = exc
        return drf_request

    def _update_user_session(self, request):
        session = request.session
        user = request.user
        if user.is_authenticated:
            current_session = get_session(
                user_id=user.id, session_key=session.session_key
            )
            if current_session:
                current_session.update_latest(
                    last_activity=session["last_activity"]
                )

    def finalize_response(self, request, response, *args, **kwargs):

        # Log all 400s
        if response.status_code >= 400:
            status_msg = (
                "status %s received by user %s attempting to access %s from %s"
                % (
                    response.status_code,
                    request.user,
                    request.path,
                    request.META.get("REMOTE_ADDR", None),
                )
            )

            if hasattr(self, "__init_request_error__"):
                response = self.handle_exception(self.__init_request_error__)
            if response.status_code == 401:
                logger.info(status_msg)
            else:
                logger.warning(status_msg)
        # TODO: check `finalize_response` getting called twice
        response = super(APIView, self).finalize_response(
            request, response, *args, **kwargs
        )

        time_started = getattr(self, "time_started", None)
        if time_started:
            self.time_elapsed = time.time() - self.time_started
            response["X-API-Time"] = "%0.3fs" % self.time_elapsed

        if not self.response_count is None:
            response["X-Total"] = int(self.response_count)

        return response

    def response(self, data=None, total=0, status=200):
        self.response_count = total
        return Response(data, status=status)

    def error(self, data=None):
        raise ValidationError({"detail": data})

    def invalid_serializer(self, serializer):
        return self.response(serializer.errors, status=400)

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            return super(APIView, self).dispatch(request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
            return self.finalize_response(request, response)

    def check_permissions(self, request):
        return super(APIView, self).check_permissions(request)

    def get_serializer(self):
        if self.serializer_class:
            return self.serializer_class(data=self.request_data)
        return None

    def invalid_serializer(self, serializer):
        return self.response(serializer.errors, status=400)

    def get_validator(self):
        if self.validator_class:
            return self.validator_class(data=self.request_data)
        return None

    def paginate(
        self, request, queryset, order_by=None, response_serializer=None
    ):
        try:
            limit = int(request.GET.get("limit", "10"))
        except ValueError:
            limit = 10
        if limit < 0 or limit > 250:
            limit = 10
        try:
            offset = int(request.GET.get("offset", "0"))
        except ValueError:
            offset = 0
        if offset < 0:
            offset = 0

        key = (
            order_by
            if order_by is None or isinstance(order_by, (list, tuple, set))
            else (order_by,)
        )
        if key:
            queryset = queryset.order_by(*key)

        results = queryset[offset : offset + limit]
        count = 0
        if response_serializer:
            count = queryset.count()
            results = response_serializer(results, many=True).data
        else:
            count = queryset.count()
        return self.response(data=results, total=count)


class APIAccessLogView(APIView):
    """Mixin to log requests"""

    logging_methods = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = {}

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.log["errors"] = traceback.format_exc()
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(
            request, response, *args, **kwargs
        )

        if self.should_log(request, response):
            if (
                connection.settings_dict.get("ATOMIC_REQUESTS")
                and getattr(response, "exception", None)
                and connection.in_atomic_block
            ):
                # response with exception (HTTP status like: 401, 404, etc)
                # pointwise disable atomic block for handle log (TransactionManagementError)
                connection.set_rollback(True)
                connection.set_rollback(False)
            if response.streaming:
                rendered_content = None
            elif hasattr(response, "rendered_content"):
                rendered_content = response.rendered_content
            else:
                rendered_content = response.getvalue()
            query_params = self._get_query_params(request) or {}
            self.log.update(
                {
                    "started_at": self.started_at,
                    "remote_addr": self._get_ip_address(request),
                    "api_view": self._get_view_name(request),
                    "view_method": self._get_view_method(request),
                    "request_path": request.path,
                    "host": request.get_host(),
                    "method": request.method,
                    "query_params": self._clean_credentials(query_params),
                    "data": self._clean_credentials(self.request_data),
                    "user": self._get_user(request),
                    "user_email": self._get_user(request).email
                    if self._get_user(request)
                    else None,
                    "time_elapsed": self.time_elapsed,
                    "response": self._clean_credentials(rendered_content),
                    "status_code": response.status_code,
                    "cf_ray_id": request.session.get("cf_ray_id", ""),
                }
            )
            if self._clean_credentials(query_params) == {}:
                self.log.update({"query_params": self.log["data"]})
            try:
                self.handle_log()
            except Exception:
                # ensure that all exceptions raised by handle_log
                # doesn't prevent API call to continue as expected
                logger.exception("Logging API call raise exception!")

        return response

    def _get_query_params(self, request):
        """
        Get query parameters
        """
        query_params = getattr(request, "query_params", None)
        if query_params:
            return query_params.dict()
        query_params = getattr(request, "GET", None)
        if query_params:
            return dict(query_params)

    def _get_ip_address(self, request):
        """Get the remote ip address the request was generated from. """
        ip = getattr(request, "ip", None)
        if ip:
            return ip
        else:
            session = request.session
            return session["ip"]

    def _get_view_name(self, request):
        """Get view name."""
        method = request.method.lower()
        try:
            attributes = getattr(self, method)
            return (
                type(attributes.__self__).__module__
                + "."
                + type(attributes.__self__).__name__
            )

        except AttributeError:
            return None

    def _get_view_method(self, request):
        """Get view method."""
        if hasattr(self, "action"):
            return self.action if self.action else None
        return request.method.lower()

    def _get_user(self, request):
        """Get user."""
        user = request.user
        if user.is_anonymous:
            return None
        return user

    def should_log(self, request, response):
        """
        Method that should return a value that evaluated to True if the request should be logged.
        By default, check if the request method is in logging_methods.
        """
        return (
            self.logging_methods == "__all__"
            or request.method in self.logging_methods
        )

    def _clean_credentials(self, data):
        """
        Cleans a dictionary of credentials of potentially sensitive info before
        sending to less secure functions.
        Reference: https://github.com/django/django/blob/stable/1.11.x/django/contrib/auth/__init__.py#L43
        """
        SENSITIVE_CREDENTIALS = re.compile(
            "api|token|key|secret|password|signature|api-key|authorization",
            re.I,
        )
        CLEANSED_SUBSTITUTE = "********************"

        if isinstance(data, bytes):
            data = data.decode(errors="replace")
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError:
                return data

        if isinstance(data, list):
            return [self._clean_credentials(d) for d in data]

        if isinstance(data, dict):
            for key in data.keys():
                search_key = str(key).lower()
                if SENSITIVE_CREDENTIALS.search(search_key):
                    data[key] = CLEANSED_SUBSTITUTE
        return data

    def handle_log(self):
        create_api_access_log(**self.log)


class LoggedInAPIView(APIAccessLogView):
    """
    LoggedInAPIView
    """

    def initialize_request(self, request, *args, **kwargs):
        """
        # TODO: Fill
        """
        exception_message = ""
        exception_class = APIException
        if not request.user.is_authenticated:
            exception_message = "User not authenticated"
            exception_class = NotAuthenticated

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)
        return drf_request


def validate_serializer(serializer):
    def validate(view_method):
        @functools.wraps(view_method)
        def handle(*args, **kwargs):
            self = args[0]
            request = args[1]
            s = serializer(data=self.request_data)
            if s.is_valid():
                # request.data = s.data
                request.data.clear()
                request.data.update(s.data)
                request.serializer = s
                return view_method(*args, **kwargs)
            else:
                return self.response(s.errors, status=400)

        return handle

    return validate
