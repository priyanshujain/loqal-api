"""
Tracking clients
"""
import json
import re

from apps.tracking.dbapi import (create_psp_api_request,
                                 create_raw_api_request,
                                 create_raw_api_response)


class PspAPIRequestTracker(object):
    psp_request = None
    raw_request = None

    def __init__(self, account_id, provider_id):
        self.account_id = account_id
        self.provider_id = provider_id

    def start_new_request(
        self,
        origin,
        endpoint,
        query_params,
        headers,
        method,
        data,
        files,
    ):
        headers = dict(headers)
        query_params = dict(query_params or {})
        self._reset_request_tracker()
        self.raw_request = create_raw_api_request(
            origin=origin,
            endpoint=endpoint,
            query_params=self._clean_credentials(query_params),
            headers=self._clean_credentials(headers),
            method=method,
            data=self._clean_credentials(data),
            files=files,
        )

        account_id = self.account_id
        psp_id = self.provider_id

        self.psp_request = create_psp_api_request(
            account_id=account_id,
            psp_id=psp_id,
            request_id=self.raw_request.id,
        )

    def _reset_request_tracker(self):
        self.raw_request = None
        self.psp_request = None

    def add_response(self, request_time_taken, status_code, headers, content):
        content = self._clean_credentials(content)
        content = self._convert_to_bytes(content)
        response = create_raw_api_response(
            request_time_taken=request_time_taken,
            status_code=status_code,
            headers=headers,
            content=content,
        )

        if response:
            self.raw_request.set_response(response=response)

    def add_errors(self, errors):
        self.psp_request.add_errors(errors)

    def add_traceback(self, tb):
        self.psp_request.add_traceback(tb)

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
            data = dict(data)
            for key in data.keys():
                search_key = str(key).lower()
                if SENSITIVE_CREDENTIALS.search(search_key):
                    data[key] = CLEANSED_SUBSTITUTE
        return data

    def _convert_to_bytes(self, data):
        """
        Convert any data to bytes
        """
        if isinstance(data, bytes):
            return bytes
        if isinstance(data, str):
            return data.encode("utf-8")
        if isinstance(data, dict) or isinstance(data, list):
            return json.dumps(data).encode("utf-8")
        else:
            return str(data).encode("utf-8")
