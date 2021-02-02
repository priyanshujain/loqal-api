from api import serializers


class CreateCampaignValidator(serializers.ValidationSerializer):
    title = serializers.CharField(max_length=256)
    short_description = serializers.CharField(max_length=1024)
    content = serializers.CharField(max_length=10 * 1024)
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()
    target_amount = serializers.DecimalField(
        min_value=1,
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
    )
