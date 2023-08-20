from rest_framework.serializers import ModelSerializer

from django_server.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]
