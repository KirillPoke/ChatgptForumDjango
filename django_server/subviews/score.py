from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from django_server.filters.score import PostScoreFilter
from django_server.models import CommentScore, PostScore
from django_server.subserializers.score import (
    CommentScoreSerializer,
    PostScoreSerializer,
)

from drf_viewset_profiler import line_profiler_viewset


@line_profiler_viewset
class ScoreViewSet(ModelViewSet):
    def get_queryset(self):
        query_params = self.request.GET.copy()
        if self.request.user.is_authenticated:
            query_params["user"] = self.request.user.id
        else:
            query_params["user"] = None
        queryset = PostScoreFilter(data=query_params, queryset=self.queryset).filter()
        return queryset

    @action(methods=["delete"], detail=False)
    def delete(self, request):
        if self.get_queryset().exists():
            self.get_queryset().first().delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["patch"], detail=False)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        upvote = serializer.validated_data["upvote"]
        if self.get_queryset().exists():
            score_instance = self.get_queryset().first()
            score_instance.upvote = upvote
            score_instance.save()
            return HttpResponse(status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


class CommentScoreViewSet(ScoreViewSet):
    queryset = CommentScore.objects.all()
    serializer_class = CommentScoreSerializer


class PostScoreViewSet(ScoreViewSet):
    queryset = PostScore.objects.all()
    serializer_class = PostScoreSerializer
