from django.db.models import Model, AutoField, ForeignKey, CASCADE, SET_NULL, DateTimeField, CharField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class User(AbstractBaseUser):
    db_table = 'users'
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

class Post(Model):
    db_table = 'posts'
    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    title = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)


class Comment(Model):
    db_table = 'comments'
    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    text = CharField(max_length=255)
    post_id = ForeignKey(Post, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
