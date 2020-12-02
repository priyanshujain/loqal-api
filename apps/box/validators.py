from django.utils.translation import gettext as _

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.box.dbapi import get_boxfile
from apps.box.models import BoxFile


class BoxFileIdSerializer(serializers.ValidationSerializer):
    id = serializers.IntegerField()
    file_name = serializers.CharField(max_length=512)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        boxfile_id = attrs.get("id")
        filter_params = {"boxfile_id": boxfile_id}
        if self.context and ("account_id" in self.context.keys()):
            filter_params["account_id"] = self.context["account_id"]
        boxfile = get_boxfile(**filter_params)
        if not boxfile:
            raise ValidationError(
                [ErrorDetail(_("Given file does not belong to account."))]
            )
        return attrs
