from django.contrib import admin

from django_server.models import Comment, Post, User

registered_models = [Comment, Post, User]
for model in registered_models:
    admin.site.register(model)