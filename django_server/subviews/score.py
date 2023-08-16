from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from django_server.models import CommentScore, PostScore
from django_server.subserializers.score import (
    CommentScoreSerializer,
    PostScoreSerializer,
)


@permission_classes([IsAuthenticated])
class CommentScoreViewSet(ModelViewSet):
    queryset = CommentScore.objects.all()
    serializer_class = CommentScoreSerializer

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        query_params["user"] = self.request.user
        return queryset


# class CommentScoreViewSet(APIView):
#     queryset = CommentScore.objects.all()
#     serializer_class = CommentScoreSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)


class PostScoreViewSet(ModelViewSet):
    queryset = PostScore.objects.all()

    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        return queryset

    serializer_class = PostScoreSerializer
