from api import serializers

__all__ = (
    "EditProfileValidator",
    "UserEmailExistsValidator",
    "UserLoginValidator",
    "ForgotPasswordValidator",
    "RequestResetPasswordValidator",
    "ResetPasswordTokenValidator",
    "ApplyResetPasswordValidator",
    "EmailVerificationValidator",
    "PhoneNumberValidator",
    "PhoneNumberCodeValidator",
    "OtpAuthValidator",
    "AvatarValidator",
)


class EditProfileValidator(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64, required=False)
    phone_number = serializers.CharField(
        max_length=20, allow_blank=True, required=False
    )
    position = serializers.CharField(
        max_length=255, allow_blank=True, required=False
    )


class UserEmailExistsValidator(serializers.ValidationSerializer):
    email = serializers.EmailField()


class UserLoginValidator(serializers.ValidationSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    tfa_code = serializers.CharField(required=False, allow_blank=True)


class OtpAuthValidator(serializers.ValidationSerializer):
    otp = serializers.CharField(required=False, max_length=6)


class PhoneNumberValidator(serializers.ValidationSerializer):
    # Add a phone_number validator
    phone_number = serializers.CharField()


class PhoneNumberCodeValidator(serializers.ValidationSerializer):
    # Add a phone_number validator
    code = serializers.CharField()


class ForgotPasswordValidator(serializers.ValidationSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class RequestResetPasswordValidator(serializers.ValidationSerializer):
    email = serializers.EmailField()


class ResetPasswordTokenValidator(serializers.ValidationSerializer):
    token = serializers.CharField()


class ApplyResetPasswordValidator(serializers.ValidationSerializer):
    token = serializers.CharField()
    password = serializers.CharField()


class EmailVerificationValidator(serializers.ValidationSerializer):
    token = serializers.CharField()


class AvatarValidator(serializers.ValidationSerializer):
    avatar_file_id = serializers.IntegerField()
