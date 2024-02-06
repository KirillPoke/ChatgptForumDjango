from rest_framework.viewsets import ModelViewSet

from django_server.models import Post
from django_server.paginators.default import DefaultPagination
from django_server.subserializers.posts import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = DefaultPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        if "page" in query_params:
            del query_params["page"]
        queryset = self.queryset.filter(**query_params)
        return queryset

    # @method_decorator(cache_page(60 * 10))
    # def list(self, *args, **kwargs):
    #     return super().list(*args, **kwargs)
