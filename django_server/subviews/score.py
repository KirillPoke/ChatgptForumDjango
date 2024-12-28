from django.http import HttpResponse
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from django_server.filters.score import PostScoreFilter
from django_server.models import CommentScore, PostScore
from django_server.subserializers.score import (
    CommentScoreSerializer,
    PostScoreSerializer,
)
from django_server.subviews.mixins.count import PostScoreCountMixin


class ScoreViewSet(AutoPrefetchViewSetMixin, ModelViewSet):
    def get_queryset(self):
        queryset = super(AutoPrefetchViewSetMixin, self).get_queryset()
        query_params = self.request.GET.copy()
        if "user_id" in query_params:
            if self.request.user.is_authenticated:
                if query_params["user_id"] != self.request.user.id:
                    raise PermissionDenied
            else:
                raise PermissionDenied
        queryset = PostScoreFilter(data=query_params, queryset=queryset).filter()
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


class PostScoreViewSet(ScoreViewSet, PostScoreCountMixin):
    queryset = PostScore.objects.all()
    serializer_class = PostScoreSerializer
