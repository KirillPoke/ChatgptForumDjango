from rest_framework.serializers import ModelSerializer
from django_server.models import CommentScore


class CommentScoreSerializer(ModelSerializer):
    class Meta:
        model = CommentScore
        fields = ['id', 'comment', 'upvote', 'created_at', 'user']


class PostScoreSerializer(ModelSerializer):
    class Meta:
        model = CommentScore
        fields = ['id', 'post', 'upvote', 'created_at', 'user']
