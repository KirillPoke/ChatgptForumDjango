from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django_server.local_settings import GOOGLE_CLIENT_SECRET
from django_server.models import User


class GoogleJWTValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        google_jwt_token = request.headers.get('Authorization')
        try:
            if google_jwt_token:
                user_data = id_token.verify_oauth2_token(google_jwt_token, Request(), GOOGLE_CLIENT_SECRET)
                user = User.objects.get(email=user_data['email'])
                request.user = user
                response = self.get_response(request)
                return response
            else:
                return self.get_response(request)
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=401)
