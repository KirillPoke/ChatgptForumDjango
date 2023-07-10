import json
from django.views import View
from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django_server.models import User
from django_server.settings import GOOGLE_CLIENT_SECRET


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


class Login(View):

    def post(self, request):
        payload = json.loads(request.body)

        try:
            user_data = get_user_data(payload.get('jwt'))  # Assuming get_user_data function is defined
        except Exception as e:
            return JsonResponse({'detail': 'Invalid token'}, status=400)

        user_query = User.objects.filter(google_id=user_data['id'])

        if user_query:
            user = user_query.first()
        else:
            user = registrate_user(user_data)
        return JsonResponse({'id': user.id, 'name': user.name, 'email': user.email}, status=200)
