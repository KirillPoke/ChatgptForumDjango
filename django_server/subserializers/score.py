from rest_framework.serializers import ModelSerializer, Serializer
from django_server.models import CommentScore


class CommentScoreSerializer(ModelSerializer):
    class Meta:
        model = CommentScore
        fields = ['id', 'comment', 'upvote']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(CommentScoreSerializer, self).create(validated_data)

class CommentScoreSearchSerializer(Serializer):


class PostScoreSerializer(ModelSerializer):
    class Meta:
        model = CommentScore
        fields = ['id', 'post', 'upvote', 'created_at', 'user']
