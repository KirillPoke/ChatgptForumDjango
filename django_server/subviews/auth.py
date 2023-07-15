from django.http import JsonResponse
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainSlidingView

from django_server.models import User
from django_server.settings import GOOGLE_CLIENT_SECRET
from django_server.subserializers.auth import JWTSerializer
from rest_framework.authtoken.models import Token


def get_user_data(token):
    # validate the token and get the user information
    idinfo = id_token.verify_oauth2_token(token, Request(), GOOGLE_CLIENT_SECRET)
    user_data = {
        'id': idinfo['sub'],
        'name': idinfo['name'],
        'email': idinfo['email']
    }
    return user_data


def registrate_user(user_data):
    new_user = User.objects.create(google_id=user_data['id'], name=user_data['name'], email=user_data['email'])
    return new_user


class Login(TokenObtainSlidingView):
    serializer_class = JWTSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = get_user_data(serializer.validated_data['jwt'])
        else:
            return JsonResponse({'detail': 'Invalid token'}, status=400)

        user_query = User.objects.filter(google_id=user_data['id'])

        if user_query:
            user = user_query.first()
        else:
            user = registrate_user(user_data)
        token = RefreshToken.for_user(user)
        response = {'id': user.id, 'name': user.name, 'email': user.email, 'access_token': str(token.access_token),
                    'refresh_token': str(token)}
        return JsonResponse(response, status=200)
