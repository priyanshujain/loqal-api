from django.db import models
from api import serializers
from apps.account.models import ConsumerAccount

__all__ = ("ConsumerAccountProfileResponse",)


class ConsumerAccountProfileResponse(serializers.ModelSerializer):
    zip_code = serializers.CharField(source="account.zip_code", read_only=True)
    class Meta:
        model = ConsumerAccount
        fields = (
            "created_at",
            "zip_code",
            "username",
        )
