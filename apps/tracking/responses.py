from re import T

from api import serializers
from apps.tracking.models import (PspApiRequestStorage, RawPspApiRequest,
                                  RawPspApiResponse)


class RawPspApiResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawPspApiResponse
        fields = "__all__"


class RawPspApiRequestSerializer(serializers.ModelSerializer):
    response = RawPspApiResponseSerializer()

    class Meta:
        model = RawPspApiRequest
        fields = "__all__"


class PspRequestAPIResponse(serializers.ModelSerializer):
    request = RawPspApiRequestSerializer()

    class Meta:
        model = PspApiRequestStorage
        fields = "__all__"


class BaseRawPspApiResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawPspApiResponse
        fields = ("status_code",)


class BaseRawPspApiRequestSerializer(serializers.ModelSerializer):
    response = BaseRawPspApiResponseSerializer()

    class Meta:
        model = RawPspApiRequest
        fields = (
            "response",
            "origin",
            "endpoint",
            "method",
        )


class BasePspRequestAPIResponse(serializers.ModelSerializer):
    request = BaseRawPspApiRequestSerializer()
    is_exception = serializers.BooleanField(
        source="exception_traceback", read_only=True
    )

    class Meta:
        model = PspApiRequestStorage
        fields = (
            "id",
            "request",
            "created_at",
            "is_exception",
        )
