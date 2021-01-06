from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.account.models import Account
from apps.provider.models import PaymentProvider
from db.models.abstract import AbstractBaseModel
from utils.shortcuts import upload_to


class APIAccessLog(AbstractBaseModel):
    """ Logs API requests """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user_email = models.EmailField(null=True, blank=True)
    started_at = models.DateTimeField(db_index=True)
    time_elapsed = models.FloatField(default=0.0)
    request_path = models.CharField(max_length=1024, db_index=True)
    api_view = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        db_index=True,
    )
    view_method = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        db_index=True,
    )
    remote_addr = models.GenericIPAddressField()
    host = models.URLField()
    ua_config = models.JSONField(null=True, blank=True)
    method = models.CharField(max_length=10)
    query_params = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True)
    cf_ray_id = models.CharField(max_length=256, blank=True)

    class Meta:
        db_table = "api_request_log"


class RawPspApiResponse(AbstractBaseModel):
    request_time_taken = models.FloatField(null=True)
    status_code = models.PositiveIntegerField(null=True, blank=True)
    headers = models.JSONField()
    content = models.TextField()

    class Meta:
        db_table = "raw_psp_api_response"


class RawPspApiRequest(AbstractBaseModel):
    origin = models.CharField(max_length=512)
    endpoint = models.CharField(max_length=512)
    query_params = models.CharField(max_length=512, blank=True)
    headers = models.JSONField()
    method = models.CharField(max_length=64)
    data = models.JSONField(null=True)
    files = ArrayField(
        models.FileField(
            upload_to=upload_to("tracking/request_files/", "file")
        ),
        default=list,
    )
    request_errors = models.TextField(null=True, blank=True)
    response = models.OneToOneField(
        RawPspApiResponse,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    def set_response(self, response):
        self.response = response
        self.save()

    class Meta:
        db_table = "raw_psp_api_request"


class PspApiRequestStorage(AbstractBaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    psp = models.ForeignKey(PaymentProvider, on_delete=models.DO_NOTHING)
    request = models.OneToOneField(
        RawPspApiRequest,
        on_delete=models.CASCADE,
    )
    api_errors = models.TextField(null=True, blank=True)
    exception_traceback = models.TextField(null=True, blank=True)

    def add_traceback(self, tb):
        self.exception_traceback = str(tb)
        self.save()

    def add_errors(self, errors):
        self.api_errors = errors
        self.save()

    class Meta:
        db_table = "psp_api_request"
