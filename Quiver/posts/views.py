from django.shortcuts import reverse, render
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
import logging as log
from django.contrib.auth import get_user_model

from .forms import PostForm, CommentForm
from .models import Post, Like, FriendRequest
from .twitter_parse import getTrending
from loginsignup.utils import getBeaverInstance, getBeaverInstanceFromUser
from loginsignup.models import Beaver

User = get_user_model()


class CreatePostView(LoginRequiredMixin, View):
    template_name = "posts/post.html"
    redirect_field_name = "next"
    form_class = PostForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        postForm = self.form_class(request.POST, request.FILES)
        if postForm.checkPost(request):
            message = "Post created successfully"
            messages.success(request, message, fail_silently=True)
            return HttpResponseRedirect(reverse("personal"))
        else:
            log.error(postForm)
            kwargs = {"form": postForm}
            return render(request, self.template_name, kwargs)


def get_hashtags(request):
    if request.is_ajax():
        response = getTrending()
        if response.get("error") is None:
            data = render_to_string(
                template_name="posts/hashtags_partial.html",
                context={"hashtags": response.get("hashtagArray")},
            )
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse(None)


class PersonalProfileView(LoginRequiredMixin, View):
    template_name = "posts/me.html"
    redirect_field_name = "next"

    def get(self, request):
        beaver = getBeaverInstance(request)
        posts = beaver.posts.all().order_by("-posted_on")
        liked = beaver.total_likes.values_list("post__id", flat=True)
        pending_requests = FriendRequest.objects.filter(receiver=beaver)
        post_liked = Post.objects.filter(pk__in=liked)
        pending_friend_requests = pending_requests[:3]
        all_requests = FriendRequest.objects.filter(
            Q(sender=beaver) | Q(receiver=beaver)
        )
        already_sent_pending = [request.user]
        for _request in all_requests:
            if beaver == _request.sender:
                already_sent_pending.append(_request.receiver.user)
            else:
                already_sent_pending.append(_request.sender.user)
        for friend in beaver.friends.all():
            already_sent_pending.append(friend.user)
        random_friends = Beaver.objects.filter(~Q(user__in=already_sent_pending))[:3]
        kwargs = {
            "profile": beaver,
            "posts": posts,
            "post_liked": post_liked,
            "random": random_friends,
            "pending": pending_friend_requests,
        }
        return render(request, self.template_name, kwargs)


class FeedView(LoginRequiredMixin, View):
    template_name = "posts/feed.html"
    redirect_field_name = "next"

    def get(self, request):
        beaver = getBeaverInstance(request)
        posts = beaver.posts.all().order_by("?")
        count = posts.count()
        friends = beaver.friends.all()
        friends_posts = Post.objects.filter(post_creator__in=friends)
        posts = posts | friends_posts
        liked = beaver.total_likes.values_list("post__id", flat=True)
        pending_requests = FriendRequest.objects.filter(receiver=beaver)
        post_liked = Post.objects.filter(pk__in=liked)
        pending_friend_requests = pending_requests[:3]
        all_requests = FriendRequest.objects.filter(
            Q(sender=beaver) | Q(receiver=beaver)
        )
        already_sent_pending = [request.user]
        for _request in all_requests:
            if beaver == _request.sender:
                already_sent_pending.append(_request.receiver.user)
            else:
                already_sent_pending.append(_request.sender.user)
        for friend in beaver.friends.all():
            already_sent_pending.append(friend.user)
        random_friends = Beaver.objects.filter(~Q(user__in=already_sent_pending))[:3]
        kwargs = {
            "profile": beaver,
            "posts": posts,
            "post_liked": post_liked,
            "random": random_friends,
            "pending": pending_friend_requests,
            "count": count,
        }
        return render(request, self.template_name, kwargs)


"""
Status

1. No pending or sent
2. Sent
3. Pending
4. Unfriend
"""


class FriendView(LoginRequiredMixin, View):
    template_name = "posts/friend_view.html"
    redirect_field_name = "next"

    def get(self, request, friend_username):
        user_beaver = getBeaverInstance(request)
        status = 1
        friend_user = User.objects.filter(username=friend_username).first()
        if friend_user is None:
            message = f"Cannot find anyone with username {friend_username}"
            messages.error(request, message, fail_silently=True)
            return HttpResponseRedirect(reverse("posts:feed"))
        beaver = getBeaverInstanceFromUser(friend_user)
        if beaver is None:
            message = f"Cannot find anyone with username {friend_username}"
            messages.error(request, message, fail_silently=True)
            return HttpResponseRedirect(reverse("posts:feed"))
        if beaver == user_beaver:
            return HttpResponseRedirect(reverse("personal"))
        if FriendRequest.objects.filter(Q(sender=user_beaver, receiver=beaver)):
            status = 2
        if FriendRequest.objects.filter(Q(sender=beaver, receiver=user_beaver)):
            status = 3
        pending_requests = FriendRequest.objects.filter(receiver=user_beaver)
        pending_friend_requests = pending_requests[:3]
        all_requests = FriendRequest.objects.filter(
            Q(sender=user_beaver) | Q(receiver=user_beaver)
        )
        already_sent_pending = [request.user]
        for _request in all_requests:
            if user_beaver == _request.sender:
                already_sent_pending.append(_request.receiver.user)
            else:
                already_sent_pending.append(_request.sender.user)
        for friend in user_beaver.friends.all():
            already_sent_pending.append(friend.user)
        random_friends = Beaver.objects.filter(~Q(user__in=already_sent_pending))[:3]
        if user_beaver.friends.filter(user=friend_user).first() is None:
            posts = beaver.posts.all().order_by("-posted_on")
            kwargs = {
                "profile": beaver,
                "posts": posts,
                "random": random_friends,
                "pending": pending_friend_requests,
                "status": status,
                "friend": False,
            }
            return render(request, self.template_name, kwargs)
        posts = beaver.posts.all().order_by("-posted_on")
        liked = user_beaver.total_likes.values_list("post__id", flat=True)
        post_liked = Post.objects.filter(pk__in=liked)
        kwargs = {
            "profile": beaver,
            "posts": posts,
            "post_liked": post_liked,
            "random": random_friends,
            "pending": pending_friend_requests,
            "status": 4,
            "friend": True,
        }
        return render(request, self.template_name, kwargs)


class UpdatePostView(LoginRequiredMixin, View):
    template_name = "posts/modify_post.html"
    redirect_field_name = "next"
    form_class = PostForm

    def get(self, request, id):
        beaver = getBeaverInstance(request)
        post = Post.objects.filter(pk=id, post_creator=beaver).first()
        if post is None:
            message = "Cannot be find the specified post"
            messages.error(request, message, fail_silently=True)
            return HttpResponseRedirect(reverse("personal"))
        kwargs = {
            "post": post,
        }
        return render(request, self.template_name, kwargs)

    def post(self, request, id):
        postForm = self.form_class(request.POST, request.FILES)
        if postForm.is_valid():
            if request.POST.get("method") == "1":
                postTemp = postForm.save(commit=False)
                beaver = getBeaverInstance(request)
                post = Post.objects.filter(pk=id, post_creator=beaver).first()
                if post is None:
                    message = "Cannot be find the specified post"
                    messages.error(request, message, fail_silently=True)
                    return HttpResponseRedirect(reverse("personal"))
                post.caption = postTemp.caption
                if postTemp.picture:
                    post.picture = postTemp.picture
                post.save()
                message = "Post Updated Successfully"
                messages.success(request, message, fail_silently=True)
                return HttpResponseRedirect(reverse("personal"))
            else:
                beaver = getBeaverInstance(request)
                post = Post.objects.filter(pk=id, post_creator=beaver).first()
                if post is None:
                    message = "Cannot find the specified post"
                    messages.error(request, message, fail_silently=True)
                    return HttpResponseRedirect(reverse("personal"))
                post.delete()
                message = "Post Deleted Successfully"
                messages.success(request, message, fail_silently=True)
                return HttpResponseRedirect(reverse("personal"))


class CommentView(LoginRequiredMixin, View):
    template_name = "posts/comment.html"
    redirect_field_name = "next"
    form_class = CommentForm

    def get(self, request, id):
        beaver = getBeaverInstance(request)
        # Can only comment on friend or their own posts
        post = Post.objects.filter(
            Q(pk=id, post_creator__in=beaver.friends.all())
            | Q(pk=id, post_creator=beaver)
        ).first()
        if post is None:
            message = "Cannot find the specified post"
            messages.error(request, message, fail_silently=True)
            return HttpResponseRedirect(reverse("personal"))
        kwargs = {
            "post": post,
        }
        return render(request, self.template_name, kwargs)

    def post(self, request, id):
        beaver = getBeaverInstance(request)
        # Can only comment on friend or their own posts
        post = Post.objects.filter(
            Q(pk=id, post_creator__in=beaver.friends.all())
            | Q(pk=id, post_creator=beaver)
        ).first()
        if post is None:
            message = "Cannot find the specified post"
            messages.error(request, message, fail_silently=True)
            return HttpResponseRedirect(reverse("personal"))
        commentForm = CommentForm(request.POST)
        if commentForm.checkComment(request, post):
            message = "Comment created successfully"
            messages.success(request, message, fail_silently=True)
            return HttpResponseRedirect(
                reverse("posts:comment", kwargs={"id": post.pk})
            )
        message = "Comment cannot be created"
        messages.error(request, message, fail_silently=True)
        return HttpResponseRedirect(reverse("posts:comment", kwargs={"id": post.pk}))


def like(request):
    if request.is_ajax():
        if not request.user:
            return JsonResponse(None)
        id = request.GET.get("id")
        beaver = getBeaverInstance(request)
        post = Post.objects.filter(
            Q(pk=id, post_creator__in=beaver.friends.all())
            | Q(pk=id, post_creator=beaver)
        ).first()
        if post is None:
            return JsonResponse(None)
        like = Like.objects.filter(post=post, liker=beaver).first()
        if like is None:
            like = Like(post=post, liker=beaver)
            like.save()
            data = {
                "status": True,
                "id": post.pk,
                "count": post.post_likes.all().count(),
            }
            log.error(data)
            return JsonResponse(data)
        else:
            like.delete()
            data = {
                "status": False,
                "id": post.pk,
                "count": post.post_likes.all().count(),
            }
            return JsonResponse(data)


def send_request(request):
    if request.is_ajax():
        if not request.user:
            return JsonResponse(None)
        username_friend = request.GET.get("username_friend")
        friend_user = User.objects.filter(username=username_friend).first()
        user_beaver = getBeaverInstance(request)
        friend_beaver = getBeaverInstanceFromUser(friend_user)
        if friend_beaver is None:
            return JsonResponse({"status": 400})
        FriendRequest.sendRequest(user_beaver, friend_beaver)
        return JsonResponse({"status": 201})


def accept_request(request):
    if not request.user:
        return JsonResponse(None)
    username_friend = request.GET.get("username_friend")
    friend_user = User.objects.filter(username=username_friend).first()
    user_beaver = getBeaverInstance(request)
    friend_beaver = getBeaverInstanceFromUser(friend_user)
    request_instance = FriendRequest.objects.filter(
        sender=friend_beaver, receiver=user_beaver
    ).first()
    if request_instance is None:
        return JsonResponse({"status": 400})
    request_instance.acceptRequest()
    return JsonResponse({"status": 201})


def reject_request(request):
    if not request.user:
        return JsonResponse(None)
    username_friend = request.GET.get("username_friend")
    friend_user = User.objects.filter(username=username_friend).first()
    user_beaver = getBeaverInstance(request)
    friend_beaver = getBeaverInstanceFromUser(friend_user)
    request_instance = FriendRequest.objects.filter(
        sender=friend_beaver, receiver=user_beaver
    ).first()
    if request_instance is None:
        return JsonResponse({"status": 400})
    request_instance.delete()
    return JsonResponse({"status": 201})


def delete_request(request):
    if not request.user:
        return JsonResponse(None)
    username_friend = request.GET.get("username_friend")
    friend_user = User.objects.filter(username=username_friend).first()
    user_beaver = getBeaverInstance(request)
    friend_beaver = getBeaverInstanceFromUser(friend_user)
    request_instance = FriendRequest.objects.filter(
        sender=user_beaver, receiver=friend_beaver
    ).first()
    if request_instance is None:
        return JsonResponse({"status": 400})
    request_instance.delete()
    return JsonResponse({"status": 201})
