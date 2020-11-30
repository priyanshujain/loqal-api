from api import serializers
from apps.account.models import Account


class AccountResponse(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "created_at",
            "id",
        )
