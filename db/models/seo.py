from django.db import models


class SeoAbstractModel(models.Model):
    title = models.CharField(max_length=70, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        abstract = True
