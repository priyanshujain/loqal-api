import os
from tempfile import NamedTemporaryFile

from celery import Task
from django.http import request
from django.utils.translation import gettext as _
from weasyprint import HTML

from api.helpers import run_validator
from apps.account.dbapi import (create_payment_account_consent,
                                get_payment_account_consent)
from apps.account.notifications import SendConsumerTermsEmail
from apps.account.validators import PaymentAccountOpeningConsentValidator
from apps.box.dbapi import create_boxfile
from apps.box.tasks import store_file_to_fss
from config.celery import app

from .create_dwolla_consumer import DwollaConsumerAccount

__all__ = ("AcceptTerms",)


class DownloadTermsDocument(object):
    def __init__(self, document_url):
        self.document_url = document_url

    def generate(self):
        f = NamedTemporaryFile(suffix=".pdf", delete=False)
        HTML(url=self.document_url).write_pdf(f.name)
        gcs_file = store_file_to_fss(f, f.name, "application/pdf")
        return f, create_boxfile(
            file_name=f.name,
            file_path=gcs_file["file_name"],
            content_type=gcs_file["content_type"],
            encryption_key=gcs_file["encryption_key"],
            document_type="payment_terms",
        )


class AcceptTermsFileTask(Task):
    name = "submit_files"

    def run(self, account_id, user_id, document_url):
        payment_consent = get_payment_account_consent(
            account_id=account_id, user_id=user_id
        )
        tempfile_obj, boxfile = DownloadTermsDocument(document_url).generate()
        SendConsumerTermsEmail(
            user=payment_consent.user, file_path=tempfile_obj.name
        ).send()
        payment_consent.add_terms_file(boxfile)


app.tasks.register(AcceptTermsFileTask)


class AcceptTerms(object):
    def __init__(self, request, data):
        self.data = data
        self.account = request.account
        self.user = request.user
        self.session = request.session
        self.ip_address = request.ip

    def handle(self):
        data = run_validator(
            PaymentAccountOpeningConsentValidator, data=self.data
        )
        is_success = DwollaConsumerAccount(
            user_id=self.user.id, ip_address=self.ip_address
        ).handle()
        if is_success:
            payment_consent = self._factory_terms_consent(data=data)
            task = AcceptTermsFileTask()
            task.delay(
                account_id=payment_consent.account.id,
                user_id=payment_consent.user.id,
                document_url=data["payment_terms_url"],
            )

    def _factory_terms_consent(self, data):
        return create_payment_account_consent(
            account_id=self.account.id,
            user_id=self.user.id,
            user_agent=self.session["user_agent"],
            ip_address=self.session["ip"],
            consent_timestamp=data["consent_timestamp"],
        )
