# TODO: Make file mangement as per sentry files
from django.db import models

from db.models.base import BaseModel


class BoxFile(BaseModel):
    file_name = models.CharField(max_length=512)
    file_path = models.CharField(max_length=512)
    content_type = models.CharField(max_length=256)
    document_type = models.CharField(max_length=512)
    encryption_key = models.CharField(max_length=64)

    def __str__(self):
        return self.file_name or "-"

    class Meta:
        db_table = "boxfile"
