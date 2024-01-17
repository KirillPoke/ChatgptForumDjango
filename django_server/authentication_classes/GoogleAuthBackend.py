import logging

from django.contrib.auth.backends import BaseBackend
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django_server.local_settings import GOOGLE_CLIENT_ID
from django_server.models import User


def registrate_user(user_data):
    try:
        new_user = User.objects.create(email=user_data["email"])
    except Exception as e:
        logging.error(f"Failed to register user, error: {e}")
        raise e
    return new_user


class GoogleAuthBackend(BaseBackend):
    def authenticate(self, request, token=None):
        if token:
            try:
                user_data = id_token.verify_oauth2_token(
                    token, Request(), GOOGLE_CLIENT_ID
                )
                try:
                    user = User.objects.get(email=user_data["email"])
                except User.DoesNotExist:
                    user = registrate_user(user_data)
                return user
            except Exception as e:
                logging.error(f"Failed to login user with google, error:{e}")
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
