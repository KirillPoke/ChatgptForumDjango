from django.contrib.auth import authenticate
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    PasswordField,
)

from django_server.settings import GOOGLE_CLIENT_ID


class JWTSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(
            write_only=True, required=False
        )
        self.fields["password"] = PasswordField(required=False)
        self.user = None

    jwt = serializers.CharField(max_length=2048, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs):
        if "jwt" in attrs:
            self.user = authenticate(token=attrs["jwt"])
            if not self.user:
                raise Exception("Failed to authenticate user")
            refresh = self.get_token(self.user)
            validated_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return validated_data
        else:
            validated_data = super().validate(attrs)
            return validated_data


def get_user_data(token):
    # validate the token and get the user information
    idinfo = id_token.verify_oauth2_token(token, Request(), GOOGLE_CLIENT_ID)
    user_data = {"id": idinfo["sub"], "name": idinfo["name"], "email": idinfo["email"]}
    return user_data
