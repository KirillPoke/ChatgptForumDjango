from rest_framework.fields import ReadOnlyField, SerializerMethodField, CharField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from django_server.models import Post, PostScore, Tag
from django_server.subserializers.tags import TagStringRelatedField


# test
class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    created_at = ReadOnlyField()
    author = StringRelatedField()
    user_score = SerializerMethodField("get_user_score", read_only=True)
    total_score = SerializerMethodField("get_total_score", read_only=True)
    tags = TagStringRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )  # PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    prompt_mode = CharField(max_length=255)

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request").user
        tags = validated_data.pop("tags")
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        return post

    def to_representation(self, obj):
        self.fields["author"] = StringRelatedField()
        return super().to_representation(obj)

    def get_user_score(self, post):
        request = self.context.get("request")
        if request.user.is_authenticated:
            try:
                post_score = PostScore.objects.get(user=request.user, post=post)
                return 1 if post_score.upvote else -1
            except PostScore.DoesNotExist:
                return 0
        else:
            return 0

    def get_total_score(self, post):
        return post.total_score

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "created_at",
            "user_score",
            "total_score",
            "chat_role",
            "tags",
            "prompt_mode",
        ]
