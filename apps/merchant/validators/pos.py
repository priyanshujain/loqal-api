from api import serializers


class CreatePosStaffValidator(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=512)
    last_name = serializers.CharField(max_length=512)
    phone_number = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=254)
    shift_start = serializers.TimeField(required=False)
    shift_end = serializers.TimeField(required=False)
    register_id = serializers.CharField(max_length=10)


class UpdatePosStaffValidator(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=512)
    last_name = serializers.CharField(max_length=512)
    phone_number = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=254)
    shift_start = serializers.TimeField(required=False)
    shift_end = serializers.TimeField(required=False)
    register_id = serializers.CharField(max_length=10)


class UpdatePosStaffMemberValidator(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=512)
    last_name = serializers.CharField(max_length=512)
    phone_number = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=254)


class PosStaffAccessTokenValidator(serializers.ValidationSerializer):
    access_token = serializers.CharField(max_length=2 * 1024)
    username = serializers.CharField(max_length=512)


class PosStaffLoginValidator(serializers.ValidationSerializer):
    access_token = serializers.CharField(max_length=2 * 1024)
    login_pin = serializers.CharField(max_length=4)
    username = serializers.CharField(max_length=512)
