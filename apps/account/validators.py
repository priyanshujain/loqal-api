from api import serializers


class RegisterAccountSerializer(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=512)
    last_name = serializers.CharField(max_length=512)
    email = serializers.EmailField(max_length=254)
    company_name = serializers.CharField(max_length=500)
    contact_number = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=64)
