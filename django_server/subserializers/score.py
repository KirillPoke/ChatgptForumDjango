from rest_framework.serializers import ModelSerializer
from django_server.models import CommentScore, PostScore


class CommentScoreSerializer(ModelSerializer):
    class Meta:
        model = CommentScore
        fields = ["comment", "upvote"]
        extra_kwargs = {"comment": {"required": False}}

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super(CommentScoreSerializer, self).create(validated_data)


class PostScoreSerializer(ModelSerializer):
    class Meta:
        model = PostScore
        fields = ["post", "upvote"]
        extra_kwargs = {"post": {"required": False}}

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super(PostScoreSerializer, self).create(validated_data)
