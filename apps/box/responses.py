from api import serializers
from apps.box.models import BoxFile


class BoxFileResponse(serializers.ModelSerializer):
    class Meta:
        model = BoxFile
        fields = (
            "file_name",
            "content_type",
            "document_type",
            "file_path",
        )
