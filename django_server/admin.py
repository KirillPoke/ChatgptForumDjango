from django.contrib import admin

from django_server.models import Comment, Post, User, CommentScore, PostScore, Tag

registered_models = [Comment, Post, User, CommentScore, PostScore, Tag]
for model in registered_models:
    admin.site.register(model)
