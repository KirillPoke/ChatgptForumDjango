from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django_server.subserializers.auth import JWTSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class Login(TokenObtainPairView):
    serializer_class = JWTSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = {"name": serializer.user.name, **serializer.validated_data}
            return JsonResponse(response, status=200)
