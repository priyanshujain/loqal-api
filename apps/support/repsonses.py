from api import serializers
from apps.support.models import SupportTicket


class SupportTicketHistoryResponse(serializers.ModelSerializer):
    issue_type = serializers.CharField(
        source="issue_type.label", read_only=True
    )

    class Meta:
        model = SupportTicket
        fields = ("created_at", "message", "issue_tracking_id", "issue_type")
