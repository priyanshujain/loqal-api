from django import forms

from api import serializers
from apps.box.models import BoxFile


class BoxFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxFile
        fields = "__all__"


class BoxFileForm(forms.Form):
    source_file = forms.FileField()
    document_type = forms.CharField()
