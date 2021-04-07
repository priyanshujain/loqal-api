from api import serializers
from apps.invite.models import C2CInvite

__all__ = ("ConsumerInviteResponse",)


class ConsumerInviteResponse(serializers.ModelSerializer):
    invite_id = serializers.CharField(source="u_id", read_only=True)

    class Meta:
        model = C2CInvite
        fields = (
            "invite_id",
            "phone_number",
            "phone_number_country",
            "email",
            "consumer_name",
            "is_used",
        )
