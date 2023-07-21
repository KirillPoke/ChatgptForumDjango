from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django_server.local_settings import GOOGLE_CLIENT_ID
from django_server.models import User
from django.contrib.auth import login
from rest_framework.authentication import BaseAuthentication


class GoogleAuthBackend(BaseBackend):

    def authenticate(self, request, token=None):
        google_jwt_token = request.headers.get('Authorization')
        try:
            if google_jwt_token:
                user_data = id_token.verify_oauth2_token(google_jwt_token, Request(), GOOGLE_CLIENT_ID)
                user = User.objects.get(email=user_data['email'])
                return user, None
                # login(request, user)
                # response = self.get_response(request)
                # return response
            else:
                return None
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def authenticate_header(self, request):
        return 'Google JWT token'
