from django.urls import path
from .views import (
    CreatePostView,
    get_hashtags,
    FeedView,
    UpdatePostView,
    FriendView,
    CommentView,
    like,
    send_request,
    accept_request,
    reject_request,
    delete_request,
)

app_name = "posts"

urlpatterns = [
    path("feed/", FeedView.as_view(), name="feed"),
    path("create/", CreatePostView.as_view(), name="create-post"),
    path("modify/<int:id>/", UpdatePostView.as_view(), name="update-post"),
    path("comment/<int:id>/", CommentView.as_view(), name="comment"),
    path("friend/<str:friend_username>/", FriendView.as_view(), name="friend"),
    path("ajax/hashtags/", get_hashtags),
    path("ajax/like/", like),
    path("ajax/send/request/", send_request),
    path("ajax/accept/request/", accept_request),
    path("ajax/reject/request/", reject_request),
    path("ajax/delete/request/", delete_request),
]
