from api import serializers
from apps.marketing.models import Campaign


class CampaignResponse(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = (
            "title",
            "short_description",
            "content",
            "starts_at",
            "ends_at",
            "target_amount",
        )
