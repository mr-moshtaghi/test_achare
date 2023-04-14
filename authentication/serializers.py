from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from authentication.models import Authenticator, User


class CellPhoneSerializer(serializers.Serializer):
    cellphone = serializers.RegexField(regex=r"^[0][9][0-9]{9}$")


class AuthenticatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authenticator
        fields = (
            'temp_token',
            'cellphone',
            'sms_verified',
            'complete',
            'expired_at',
            'created_at',
        )


class VerifySmsTokenSerializer(serializers.Serializer):
    sms_token = serializers.IntegerField()


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=255,
    )
    last_name = serializers.CharField(
        max_length=255,
    )
    password = serializers.CharField(
        max_length=255
    )
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError(
                _('Email already exists')
            )


class LoginSerializer(serializers.Serializer):
    cellphone = serializers.RegexField(regex=r"^[0][9][0-9]{9}$")
    password = serializers.CharField(max_length=255)
