from rest_framework.fields import ReadOnlyField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from django_server.models import Post


class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    created_at = ReadOnlyField()
    author = StringRelatedField()

    class Meta:
        model = Post
        fields = ["id", "author", "title", "created_at"]
