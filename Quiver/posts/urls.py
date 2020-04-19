from django.urls import path, re_path
from .views import CreatePostView, get_hashtags, FeedView, UpdatePostView

app_name = "posts"

urlpatterns = [
    path("feed/", FeedView.as_view(), name="feed"),
    path("create/", CreatePostView.as_view(), name="create-post"),
    path("modify/<int:id>/", UpdatePostView.as_view(), name="update-post"),
    path("ajax/hashtags/", get_hashtags),
]