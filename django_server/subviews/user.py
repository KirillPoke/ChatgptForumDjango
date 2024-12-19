from django_server.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes

from django_server.authentication_classes.permissions import AllowOwner
from django_server.subserializers.user import UserSerializer

from drf_viewset_profiler import line_profiler_viewset


@line_profiler_viewset
@permission_classes([AllowOwner])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "name"

    def get_queryset(self):
        queryset = self.queryset.filter(id=self.request.user.id)
        return queryset
