from rest_framework.viewsets import ModelViewSet

from django_server.models import Post
from django_server.subserializers.posts import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        return queryset

    serializer_class = PostSerializer
