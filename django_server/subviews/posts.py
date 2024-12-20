from django.db.models import F
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework.viewsets import ModelViewSet

from django_server.models import Post
from django_server.paginators.default import DefaultPagination
from django_server.subserializers.posts import PostSerializer


class PostViewSet(AutoPrefetchViewSetMixin, ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = DefaultPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super(AutoPrefetchViewSetMixin, self).get_queryset()
        queryset = (
            queryset.prefetch_related("author")
            .all()
            .annotate(authore=F("author__name"))
        )
        query_params = self.request.query_params.dict()
        if "page" in query_params:
            del query_params["page"]
        queryset = queryset.filter(**query_params)
        return queryset
