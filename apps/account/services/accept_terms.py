import os
from tempfile import NamedTemporaryFile

import pdfkit
from django.utils.translation import gettext as _

from api.helpers import run_validator
from apps.account.dbapi import create_payment_account_consent
from apps.account.validators import PaymentAccountOpeningConsentValidator
from apps.box.dbapi import create_boxfile
from apps.box.tasks import store_file_to_gcs

__all__ = ("AcceptTerms",)


class AcceptTerms(object):
    def __init__(self, request, data):
        self.data = data
        self.account = request.account
        self.user = request.user
        self.session = request.session

    def handle(self):
        data = run_validator(
            PaymentAccountOpeningConsentValidator, data=self.data
        )
        boxfile = DownloadTermsDocument(
            document_url=data["payment_terms_url"]
        ).generate()
        self._factory_terms_consent(data=data, boxfile=boxfile)

    def _factory_terms_consent(self, data, boxfile):
        return create_payment_account_consent(
            account_id=self.account.id,
            user_id=self.user.id,
            user_agent=self.session["user_agent"],
            ip_address=self.session["ip"],
            consent_timestamp=data["consent_timestamp"],
            payment_term_document_id=boxfile.id,
        )


class DownloadTermsDocument(object):
    def __init__(self, document_url):
        self.document_url = document_url

    def generate(self):
        f = NamedTemporaryFile(suffix=".pdf")
        pdfkit.from_url(self.document_url, f.name)
        gcs_file = store_file_to_gcs(f, f.name, "application/pdf")
        os.unlink(f.name)
        return create_boxfile(
            file_name=f.name,
            file_path=gcs_file["file_name"],
            content_type=gcs_file["content_type"],
            encryption_key=gcs_file["encryption_key"],
            document_type="payment_terms",
        )
