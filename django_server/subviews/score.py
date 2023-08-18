from django_server.models import CommentScore, PostScore
from django_server.subserializers.score import (
    CommentScoreSerializer,
    PostScoreSerializer,
)
from django_server.subviews.base import ScoreViewSet


class CommentScoreViewSet(ScoreViewSet):
    queryset = CommentScore.objects.all()
    serializer_class = CommentScoreSerializer


class PostScoreViewSet(ScoreViewSet):
    queryset = PostScore.objects.all()
    serializer_class = PostScoreSerializer
