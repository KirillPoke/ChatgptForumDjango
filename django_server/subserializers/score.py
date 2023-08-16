from django.forms import BooleanField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer
from django_server.models import CommentScore


class CommentScoreSerializer(ModelSerializer):
    class Meta:
        model = CommentScore
        fields = ["id", "comment", "upvote"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super(CommentScoreSerializer, self).create(validated_data)


class CommentScoreSearchSerializer(Serializer):
    comment_id = PrimaryKeyRelatedField(many=True, read_only=True)
    upvote = BooleanField()

    def to_internal_value(self, data):
        print(1)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super(CommentScoreSearchSerializer, self).create(validated_data)


class PostScoreSerializer(ModelSerializer):
    class Meta:
        model = CommentScore
        fields = ["id", "post", "upvote", "created_at", "user"]
