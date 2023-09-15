from django.db.models import (
    Model,
    AutoField,
    ForeignKey,
    CASCADE,
    SET_NULL,
    DateTimeField,
    CharField,
    TextField,
    BooleanField,
    EmailField,
    ManyToManyField,
)
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from random_username.generate import generate_username
from tree_queries.models import TreeNode

from django_server.ai.Completions import generate_completion_prompt
from django_server.ai.PromptInitiator import allow_score_based_prompt


class GoogleUserManager(UserManager):
    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        del extra_fields["is_staff"]
        return self._create_user(email, email, password, **extra_fields)


def get_default_user_display_name():
    return generate_username()[0]


class User(AbstractBaseUser, PermissionsMixin):
    id = AutoField(primary_key=True)
    email = EmailField(unique=True)
    google_id = CharField(max_length=255, unique=True)
    name = CharField(max_length=255, unique=True, default=get_default_user_display_name)
    created_at = DateTimeField(auto_now_add=True)
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    USERNAME_FIELD = "email"
    objects = GoogleUserManager()

    def __str__(self):
        return self.name

    @staticmethod
    def owner_field():
        return "id"


class Tag(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(Model):
    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    title = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    chat_role = TextField(max_length=65535, default="You are a helpful assistant.")
    tags = ManyToManyField(Tag)

    def __str__(self):
        return f"{self.id}|{self.title}"

    @staticmethod
    def owner_field():
        return "author"

    @property
    def total_score(self):
        query = PostScore.objects.filter(post=self)
        upvotes = query.filter(upvote=True).count()
        downvotes = query.filter(upvote=False).count()
        return upvotes - downvotes


class Comment(TreeNode):
    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    text = TextField(max_length=65535)
    post = ForeignKey(Post, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_prompt = BooleanField(default=False)

    @staticmethod
    def owner_field():
        return "author"

    @property
    def total_score(self):
        query = CommentScore.objects.filter(comment=self)
        upvotes = query.filter(upvote=True).count()
        downvotes = query.filter(upvote=False).count()
        return upvotes - downvotes


class CommentScore(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=CASCADE)
    upvote = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    comment = ForeignKey(Comment, on_delete=CASCADE)

    @staticmethod
    def owner_field():
        return "user"

    class Meta:
        unique_together = ("user", "comment")


@receiver(post_save, sender=CommentScore)
def call_check_crowd_based_vote(sender, instance, **kwargs):
    if allow_score_based_prompt(instance.comment):
        generate_completion_prompt(instance.comment)


class PostScore(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=CASCADE)
    upvote = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    post = ForeignKey(Post, on_delete=CASCADE)

    class Meta:
        unique_together = ("user", "post")

    @staticmethod
    def owner_field():
        return "user"
