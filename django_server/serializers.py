from rest_framework.serializers import ModelSerializer, ReadOnlyField

from django_server.models import Comment, Post


class CommentSerializer(ModelSerializer):
    id = ReadOnlyField()
    post_id = ReadOnlyField()
    author = ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'author', 'text']


class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    created_at = ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'created_at']