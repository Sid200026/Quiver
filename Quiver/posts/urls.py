from django.urls import path
from .views import (
    CreatePostView,
    get_hashtags,
    FeedView,
    UpdatePostView,
    CommentView,
    like,
)

app_name = "posts"

urlpatterns = [
    path("feed/", FeedView.as_view(), name="feed"),
    path("create/", CreatePostView.as_view(), name="create-post"),
    path("modify/<int:id>/", UpdatePostView.as_view(), name="update-post"),
    path("comment/<int:id>/", CommentView.as_view(), name="comment"),
    path("ajax/hashtags/", get_hashtags),
    path("ajax/like/", like),
]
