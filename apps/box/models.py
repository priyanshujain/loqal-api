# TODO: Make file mangement as per sentry files
from django.db import models

from db.models import BaseModel


# TODO: src/sentry/models/file.py
class BoxFile(BaseModel):
    file_name = models.CharField(max_length=512)
    file_path = models.CharField(max_length=512)
    content_type = models.CharField(max_length=256)
    document_type = models.CharField(max_length=512)
    encryption_key = models.CharField(max_length=64)
    in_use = models.BooleanField(default=False)

    def __str__(self):
        return self.file_name or "-"

    def enable_use(self):
        self.in_use = True
        self.save()

    class Meta:
        db_table = "boxfile"
