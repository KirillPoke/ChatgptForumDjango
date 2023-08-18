from rest_framework.viewsets import ModelViewSet

from django_server.models import Post
from django_server.subserializers.posts import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
