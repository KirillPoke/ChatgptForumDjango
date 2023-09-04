"""
URL configuration for django_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from django_server.subviews.auth import Login
from django_server.subviews.score import CommentScoreViewSet, PostScoreViewSet
from django_server.subviews.posts import PostViewSet
from django_server.subviews.comments import CommentViewSet
from django_server.subviews.user import UserViewSet

router = routers.DefaultRouter()
router.register("comments", CommentViewSet)
router.register("posts", PostViewSet)
router.register("comment_score", CommentScoreViewSet)
router.register("post_score", PostScoreViewSet)
router.register("users", UserViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", Login.as_view(), name="login"),
    path("", include(router.urls)),
    path("accounts/", include("allauth.urls")),
]
