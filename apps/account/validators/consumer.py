"""
Validators for consumer APIs
"""
from api import serializers

__all__ = ("CreateConsumerAccountValidator",)


class CreateConsumerAccountValidator(serializers.ValidationSerializer):
    """
    Validate consumer account
    """

    first_name = serializers.CharField(max_length=512)
    last_name = serializers.CharField(max_length=512)
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=64)
