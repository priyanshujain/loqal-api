from api import serializers
from apps.account.models import Account

__all__ = (
    "ConsumerAccountProfileResponse",
)

class ConsumerAccountProfileResponse(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = (
            "created_at",
            "id",
            "zip_code",
        )
