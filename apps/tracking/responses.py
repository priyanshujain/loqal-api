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
