from api import serializers
from lib.auth import password_validation

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
    "OtpAuthValidator",
    "AvatarValidator",
    "VerifyPhoneNumberOtpValidator",
    "ResendPhoneNumberOtpValidator",
)


class EditProfileValidator(serializers.ValidationSerializer):
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)


class UserEmailExistsValidator(serializers.ValidationSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["email"] = str(attrs["email"]).lower()
        return attrs


class UserLoginValidator(serializers.ValidationSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    tfa_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["email"] = str(attrs["email"]).lower()
        return attrs


class OtpAuthValidator(serializers.ValidationSerializer):
    otp = serializers.CharField(required=False, max_length=6)


class PhoneNumberValidator(serializers.ValidationSerializer):
    # Add a phone_number validator
    phone_number = serializers.CharField(max_length=10)
    secret = serializers.CharField()


class VerifyPhoneNumberOtpValidator(serializers.ValidationSerializer):
    otp = serializers.CharField(required=False, max_length=6)
    secret = serializers.CharField()


class ResendPhoneNumberOtpValidator(serializers.ValidationSerializer):
    secret = serializers.CharField()


class ForgotPasswordValidator(serializers.ValidationSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, new_password):
        password_validation.validate_password(new_password)
        return new_password


class RequestResetPasswordValidator(serializers.ValidationSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["email"] = str(attrs["email"]).lower()
        return attrs


class ResetPasswordTokenValidator(serializers.ValidationSerializer):
    token = serializers.CharField()


class ApplyResetPasswordValidator(serializers.ValidationSerializer):
    token = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password


class EmailVerificationValidator(serializers.ValidationSerializer):
    token = serializers.CharField()


class AvatarValidator(serializers.ValidationSerializer):
    avatar_file_id = serializers.IntegerField()
