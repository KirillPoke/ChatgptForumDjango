import logging

from django.contrib.auth.backends import BaseBackend
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django_server.local_settings import GOOGLE_CLIENT_ID
from django_server.models import User


def registrate_user(user_data):
    new_user = User.objects.create(name=user_data["name"], email=user_data["email"])
    return new_user


class GoogleAuthBackend(BaseBackend):
    def authenticate(self, request, token=None):
        logging.info(f"got token, length: {len(str(token))}")
        if token:
            try:
                user_data = id_token.verify_oauth2_token(
                    token, Request(), GOOGLE_CLIENT_ID
                )
                logging.info(f"email: {user_data.get('email', 'no email')}")
                try:
                    user = User.objects.get(email=user_data["email"])
                except User.DoesNotExist:
                    logging.info("registrating user")
                    user = registrate_user(user_data)
                return user
            except Exception:
                return None
        else:
            logging.info("no token")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
