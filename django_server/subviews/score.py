from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from django_server.models import CommentScore, PostScore
from django_server.subserializers.score import (
    CommentScoreSerializer,
    PostScoreSerializer,
)


@permission_classes([IsAuthenticated])
class CommentScoreViewSet(ModelViewSet):
    queryset = CommentScore.objects.all()
    serializer_class = CommentScoreSerializer

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        query_params["user"] = self.request.user
        return queryset


class PostScoreViewSet(ModelViewSet):
    queryset = PostScore.objects.all()

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        return queryset

    serializer_class = PostScoreSerializer
