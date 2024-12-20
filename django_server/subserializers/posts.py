from rest_framework.fields import ReadOnlyField, SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from django_server.models import Post, Tag
from django_server.subserializers.tags import TagStringRelatedField


# test
class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    created_at = ReadOnlyField()
    author = CharField(source="author.name", read_only=True)
    total_score = SerializerMethodField("get_total_score", read_only=True)
    tags = TagStringRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    prompt_mode = CharField(max_length=255)

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request").user
        tags = validated_data.pop("tags")
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        return post

    # def to_representation(self, obj):
    #     self.fields["author"] = StringRelatedField()
    #     return super().to_representation(obj)

    def get_total_score(self, post):
        return post.total_score

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "created_at",
            "total_score",
            "chat_role",
            "tags",
            "prompt_mode",
        ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance is not None and not hasattr(self.instance, '_prefetched_objects_cache'):
    #         # Add select_related to optimize the query
    #         if isinstance(self.instance, QuerySet):
    #             self.instance = self.instance.select_related('author')
