from django.db.models.signals import post_save
from django.dispatch import receiver

from django_server.ai.Completions import generate_completion_prompt
from django_server.models import Comment, CommentScore

COMMENT_SCORE_TO_POST_SCORE_RATIO = 10
COMMENT_SCORE_TO_PARENT_SCORE_RATIO = 2
MINIMUM_COMMENT_SCORE = 5


def eligible_for_prompt(comment: Comment) -> bool:
    comment_score = comment.total_score
    if comment_score < MINIMUM_COMMENT_SCORE:
        return False
    if comment.parent:
        if (
            comment.total_score * COMMENT_SCORE_TO_PARENT_SCORE_RATIO
            >= comment.parent.total_score
        ):
            return True
    else:
        post = comment.post
        if comment.total_score * 10 >= post.total_score:
            return True


@receiver(post_save, sender=CommentScore)
def check_prompt_eligibility(sender, instance, **kwargs):
    if eligible_for_prompt(instance.comment):
        generate_completion_prompt(instance.comment)
