from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from django_server.models import Post, Comment


class CommentSerializer(ModelSerializer):
    id = ReadOnlyField()
    post_id = PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = StringRelatedField()

    class Meta:
        model = Comment
        fields = ["id", "post_id", "author", "text", "is_prompt"]


class CommentSerializerPost(CommentSerializer):
    author = SerializerMethodField("_user")

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request:
            validated_data["author"] = request.user
        return super().create(validated_data)

    def _user(self, obj):
        request = self.context.get("request", None)
        if request:
            return str(request.user)
