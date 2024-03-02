from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from django_server.subserializers.auth import JWTSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


class Login(TokenObtainPairView):
    serializer_class = JWTSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = {"name": serializer.user.name, **serializer.validated_data}
            return JsonResponse(response, status=status.HTTP_200_OK)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://www.geppetaboard.com/"
    client_class = OAuth2Client
