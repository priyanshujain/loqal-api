from django.utils.translation import gettext as _
from django import forms

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.box.dbapi import get_boxfile


class BoxFileIdSerializer(serializers.ValidationSerializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        boxfile_id = attrs.get("id")
        filter_params = {"boxfile_id": boxfile_id}
        boxfile = get_boxfile(**filter_params)
        if not boxfile:
            raise ValidationError(
                [ErrorDetail(_("Given file does not exist."))]
            )
        return attrs


class BoxFileForm(forms.Form):
    source_file = forms.FileField()
    document_type = forms.CharField()
