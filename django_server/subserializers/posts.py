from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from django_server.models import Post, PostScore


class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    created_at = ReadOnlyField()
    author = StringRelatedField()
    user_score = SerializerMethodField("get_user_score")

    def get_user_score(self, comment):
        request = self.context.get("request")
        if request.user.is_authenticated:
            try:
                comment_score = PostScore.objects.get(
                    user=request.user, comment=comment
                )
                return 1 if comment_score.upvote else -1
            except PostScore.DoesNotExist:
                return 0
        else:
            return 0

    class Meta:
        model = Post
        fields = ["id", "author", "title", "created_at"]
