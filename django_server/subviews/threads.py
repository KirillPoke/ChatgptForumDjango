from requests import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django_server.models import Comment, Post
from django_server.serializers import CommentSerializer, CommentSerializerPost, PostSerializer
from django_server.ai.Completions import ai_comment


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CommentSerializer
        else:
            return CommentSerializerPost

    def update(self, request, *args, **kwargs):
        patch_serializer = self.get_serializer_class()(data=request.data, partial=True)
        patch_serializer.is_valid(raise_exception=True)
        try:
            comment = Comment.objects.get(id=kwargs['pk'])
            if 'is_prompt' in patch_serializer.validated_data:
                comment.is_prompt = patch_serializer.validated_data['is_prompt']
                comment.save()
            ai_comment(comment)
        except Comment.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(status=200)

    # def list(self, request, *args, **kwargs):
    #     return HttpResponse(status=200)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
