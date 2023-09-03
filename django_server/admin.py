from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django_server.models import Comment, Post, User, CommentScore, PostScore, Tag


class CustomUserAdmin(UserAdmin):
    # Customize the UserAdmin class as needed
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "groups")
    search_fields = ("username", "email")
    ordering = ("-id",)
    fieldsets = ((None, {"fields": ("email", "password")}),)


registered_models = [Comment, Post, CommentScore, PostScore, Tag]
for model in registered_models:
    admin.site.register(model)
admin.site.register(User, CustomUserAdmin)
