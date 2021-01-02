from api import serializers
from apps.box.models import BoxFile


class BoxFileResponse(serializers.ModelSerializer):
    class Meta:
        model = BoxFile
        fields = "__all__"
