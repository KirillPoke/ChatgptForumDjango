from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
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


class PostMetaViewSet(GenericAPIView):
    model = Post

    def get_meta_data(self, fields):
        metadata_handlers = {"count": lambda: self.model.objects.count()}
        metadata_dict = dict()
        for field in fields:
            metadata_dict[field] = metadata_handlers[field]()
        return metadata_dict

    def get(self, request):
        fields_to_return = request.query_params.dict().get("fields").split(",")
        return JsonResponse(
            self.get_meta_data(fields_to_return), status=status.HTTP_200_OK, safe=False
        )
