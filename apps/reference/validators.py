from api import serializers


class CitySearchSerializer(serializers.ValidationSerializer):
    """Validate req"""

    # TODO: add validations for all these fields
    country = serializers.CharField(max_length=2)
    city = serializers.CharField(max_length=256)


class RegionStateSerializer(serializers.ValidationSerializer):
    """Validate req"""

    # TODO: add validations for all these fields
    country = serializers.CharField(max_length=2)
