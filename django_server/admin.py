from django.contrib import admin

from django_server.models import Comment, Post, User, CommentScore, PostScore

registered_models = [Comment, Post, User, CommentScore, PostScore]
for model in registered_models:
    admin.site.register(model)
