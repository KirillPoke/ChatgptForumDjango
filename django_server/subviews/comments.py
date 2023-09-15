from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from django_server.ai.Completions import generate_completion_prompt
from django_server.models import Comment
from django_server.subserializers.comments import (
    CommentSerializer,
    CommentSerializerPost,
)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by("id")

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommentSerializer
        else:
            return CommentSerializerPost

    def update(self, request, *args, **kwargs):
        patch_serializer = self.get_serializer_class()(data=request.data, partial=True)
        patch_serializer.is_valid(raise_exception=True)
        try:
            comment = Comment.objects.get(id=kwargs["pk"])
            if "is_prompt" in patch_serializer.validated_data:
                comment.is_prompt = patch_serializer.validated_data["is_prompt"]
                comment.save()
            generate_completion_prompt(comment)
        except Comment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        return HttpResponse(status.HTTP_200_OK)


def serialize_tree(qs, d):
    if not qs:
        return []
    for node in qs:
        d[node.id] = model_to_dict(node)
        d[node.id]["children"] = {}
        serialize_tree(node.children.with_tree_fields(), d[node.id]["children"])


class CommentTree(GenericAPIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        model_list = list(Comment.objects.filter(**query_params).with_tree_fields())
        response_data = []
        for instance in model_list:
            serializer = CommentSerializer(instance, context={"request": request})
            model_dict = serializer.data
            model_dict["tree_path"] = instance.tree_path
            response_data.append(model_dict)
        return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)
