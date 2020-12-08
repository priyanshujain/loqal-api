"""
requests exceptions
"""
from requests.exceptions import ChunkedEncodingError  # Errors; Warnings
from requests.exceptions import (ConnectionError, ConnectTimeout,
                                 ContentDecodingError, FileModeWarning,
                                 HTTPError, InvalidHeader, InvalidProxyURL,
                                 InvalidSchema, InvalidURL, MissingSchema,
                                 ProxyError, ReadTimeout, RequestException,
                                 RequestsDependencyWarning, RequestsWarning,
                                 RetryError, SSLError, StreamConsumedError,
                                 Timeout, TooManyRedirects,
                                 UnrewindableBodyError, URLRequired)
