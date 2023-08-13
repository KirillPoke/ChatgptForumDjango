from rest_framework.viewsets import ModelViewSet

from django_server.models import CommentScore, PostScore
from django_server.subserializers.score import CommentScoreSerializer, PostScoreSerializer


class CommentScoreViewSet(ModelViewSet):
    queryset = CommentScore.objects.all()

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        return queryset

    serializer_class = CommentScoreSerializer


class PostScoreViewSet(ModelViewSet):
    queryset = PostScore.objects.all()

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        return queryset

    serializer_class = PostScoreSerializer
