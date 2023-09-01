from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from django_server.models import Post, Comment, CommentScore


class CommentSerializer(ModelSerializer):
    id = ReadOnlyField()
    post = PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = StringRelatedField()
    user_score = SerializerMethodField("get_user_score")
    parent_comment = PrimaryKeyRelatedField(queryset=Comment.objects.all())

    def get_user_score(self, comment):
        request = self.context.get("request")
        if request.user.is_authenticated:
            try:
                comment_score = CommentScore.objects.get(
                    user=request.user, comment=comment
                )
                return 1 if comment_score.upvote else -1
            except CommentScore.DoesNotExist:
                return 0
        else:
            return 0

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "text",
            "is_prompt",
            "user_score",
            "parent_comment",
        ]


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
