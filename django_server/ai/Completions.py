import logging

from openai import ChatCompletion
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_server.ai.PromptEligibility import eligible_for_prompt
from django_server.models import Comment, CommentScore


def generate_chat_history(comment):
    messages_list = [
        {"role": "system", "content": comment.post.chat_role},
    ]
    previous_comments = comment.ancestors(include_self=True)
    tree_depth = comment.ancestors(include_self=True).count()
    slice_index = 0 if tree_depth <= 5 else tree_depth - 5
    sliced_previous_comments = previous_comments[slice_index:]
    sliced_previous_comments = sliced_previous_comments.values_list(
        "text", "author"
    )  # For now limit to 5 messages, TODO: make it dynamic based on token usage of comments
    for comment in sliced_previous_comments:
        if comment[1] is None:
            messages_list.append({"role": "assistant", "content": comment[0]})
        else:
            messages_list.append({"role": "user", "content": comment[0]})
    return messages_list


def create_ai_comment(message_history):
    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
        max_tokens=512,
    )
    comment_text = response.choices[0].message["content"]
    return comment_text
    # return "Dummy ai comment"


def generate_completion_prompt(comment):
    message_history = generate_chat_history(comment)
    comment_text = create_ai_comment(message_history)
    Comment.objects.create(
        text=comment_text, post=comment.post, parent=comment, author=None
    )


@receiver(post_save, sender=CommentScore)
def check_prompt_eligibility(sender, instance, **kwargs):
    if eligible_for_prompt(instance.comment):
        logging.info(
            f"Comment was submitted as a prompt, id: {instance.comment.id}, score: {instance.comment.total_score}"
        )
        generate_completion_prompt(instance.comment)
        instance.comment.is_prompt = True
        instance.comment.save()
