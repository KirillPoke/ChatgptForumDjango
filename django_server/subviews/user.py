from rest_framework.authtoken.admin import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes

from django_server.authentication_classes.permissions import AllowOwner
from django_server.subserializers.user import UserSerializer


@permission_classes([AllowOwner])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
