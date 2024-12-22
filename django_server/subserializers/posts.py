from rest_framework.fields import ReadOnlyField, CharField
from rest_framework.serializers import ModelSerializer

from django_server.models import Post
from django_server.subserializers.mixins.selected_fields import SelectedFieldsMixin


# test
class PostSerializer(SelectedFieldsMixin, ModelSerializer):
    id = ReadOnlyField()
    created_at = ReadOnlyField()
    author = CharField(source="author.name", read_only=True)
    # total_score = SerializerMethodField("get_total_score", read_only=True)
    prompt_mode = CharField(max_length=255)

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request").user
        tags = validated_data.pop("tags")
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        return post

    def get_total_score(self, post):
        return post.total_score

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "created_at",
            # "total_score",
            "chat_role",
            "prompt_mode",
        ]
