from django.http import HttpResponse
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


@permission_classes([IsAuthenticated])
class ScoreViewSet(ModelViewSet):
    def get_queryset(self):
        query_params = self.request.query_params.dict()
        queryset = self.queryset.filter(**query_params)
        query_params["user"] = self.request.user
        return queryset

    @action(methods=["delete"], detail=False)
    def delete(self, request):
        if self.queryset.exists():
            self.queryset.first().delete()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)

    @action(methods=["patch"], detail=False)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        upvote = serializer.validated_data["upvote"]
        if self.queryset.exists():
            self.queryset.first().upvote = upvote
            self.queryset.first().save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
