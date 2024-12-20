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
        query_params = self.request.query_params.dict()
        if "page" in query_params:
            del query_params["page"]
        queryset = queryset.filter(**query_params)
        return queryset

    # TODO: Add caching if needed to speed up homepage
    # def list(self, request, *args, **kwargs):
    #     cached_data = cache.get("home_page_posts")
    #     if cached_data:
    #         return Response(cached_data)
    #     else:
    #         queryset = self.filter_queryset(self.get_queryset())
    #
    #         page = self.paginate_queryset(queryset)
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             response = self.get_paginated_response(serializer.data)
    #             cache.set("home_page_posts", response.data, 60)
    #             return response
    #
    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(serializer.data)
