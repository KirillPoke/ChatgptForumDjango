from rest_framework.viewsets import ModelViewSet

from django_server.models import Comment, Post
from django_server.serializers import CommentSerializer, PostSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
