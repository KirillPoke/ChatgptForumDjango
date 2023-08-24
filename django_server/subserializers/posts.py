from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from django_server.models import Post, PostScore


class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    created_at = ReadOnlyField()
    author = StringRelatedField()
    user_score = SerializerMethodField("get_user_score", read_only=True)
    total_score = SerializerMethodField("get_total_score", read_only=True)

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request").user
        return Post.objects.create(**validated_data)

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
        query = PostScore.objects.filter(post=post)
        upvotes = query.filter(upvote=True).count()
        downvotes = query.filter(upvote=False).count()
        return upvotes - downvotes

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
        ]
