from django.http import JsonResponse
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from django_server.models import User
from django_server.settings import GOOGLE_CLIENT_ID
from django_server.subserializers.auth import JWTSerializer


def get_user_data(token):
    # validate the token and get the user information
    idinfo = id_token.verify_oauth2_token(token, Request(), GOOGLE_CLIENT_ID)
    user_data = {"id": idinfo["sub"], "name": idinfo["name"], "email": idinfo["email"]}
    return user_data


def registrate_user(user_data):
    new_user = User.objects.create(
        google_id=user_data["id"], name=user_data["name"], email=user_data["email"]
    )
    return new_user


class Login(GenericAPIView):
    serializer_class = JWTSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = get_user_data(serializer.validated_data["jwt"])
        else:
            return JsonResponse({"detail": "Invalid token"}, status=400)

        user_query = User.objects.filter(google_id=user_data["id"])

        if user_query:
            user = user_query.first()
        else:
            user = registrate_user(user_data)
        response = {"id": user.id, "name": user.name}
        return JsonResponse(response, status=200)
