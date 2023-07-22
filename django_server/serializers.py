from rest_framework.relations import SlugRelatedField, StringRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, ReadOnlyField

from django_server.models import Comment, Post, User


class CommentSerializer(ModelSerializer):
    id = ReadOnlyField()
    post_id = PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'author', 'text']


class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    created_at = ReadOnlyField()
    author = StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'created_at']
