from requests import Response
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django_server.models import Comment, Post
from django_server.serializers import CommentSerializer, CommentSerializerPost, PostSerializer
from django_server.ai.Completions import ai_comment


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CommentSerializer
        else:
            return CommentSerializerPost

    def update(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=kwargs['pk'])
            ai_comment(comment)
        except Comment.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(status=200)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
