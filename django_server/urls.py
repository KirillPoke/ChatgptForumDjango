from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static

from django_server import settings
from django_server.subviews.score import CommentScoreViewSet, PostScoreViewSet
from django_server.subviews.posts import PostViewSet
from django_server.subviews.comments import CommentViewSet, CommentTree
from django_server.subviews.user import UserViewSet

router = routers.DefaultRouter()
router.register("comments", CommentViewSet)
router.register("posts", PostViewSet)
router.register("comment_score", CommentScoreViewSet, basename="CommentScore")
router.register("post_score", PostScoreViewSet, basename="PostScore")
router.register("users", UserViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("comments/tree", CommentTree.as_view(), name="comments_tree"),
    path("", include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
