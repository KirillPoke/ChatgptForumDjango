from django_server.models import Comment, SCORE

COMMENT_SCORE_TO_POST_SCORE_RATIO = 10
COMMENT_SCORE_TO_PARENT_SCORE_RATIO = 2
MINIMUM_COMMENT_SCORE = 3


def eligible_for_prompt(comment: Comment) -> bool:
    if comment.post.prompt_mode != SCORE:
        return False
    if not comment.author:  # Don't make prompts out of ai comments
        return False
    if comment.is_prompt:
        return False
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
