from api import serializers


class CheckRewardSerializer(serializers.ValidationSerializer):
    merchant_id = serializers.UUIDField()
