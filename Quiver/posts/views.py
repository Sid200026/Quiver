from django.shortcuts import reverse, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
import logging as log

from .forms import PostForm
from .models import Post
from .twitter_parse import getTrending
from loginsignup.utils import getBeaverInstance


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
            return HttpResponseRedirect(reverse("posts:feed"))
        else:
            log.error(postForm)
            kwargs = {"form": postForm}
            return render(request, self.template_name, kwargs)


def get_hashtags(request):
    if request.is_ajax():
        response = getTrending()
        if response.get("error") == None:
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
        posts = beaver.posts.all().order_by('posted_on')
        kwargs = {
            'profile': beaver,
            'posts': posts
        }
        return render(request, self.template_name, kwargs)

class FeedView(LoginRequiredMixin, View):
    template_name = "posts/feed.html"
    redirect_field_name = "next"

    def get(self, request):
        beaver = getBeaverInstance(request)
        kwargs = {
            'profile': beaver,
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
            return HttpResponseRedirect(reverse("posts:feed"))
        kwargs = {
            "post":post,
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
                    return HttpResponseRedirect(reverse("posts:feed"))
                post.caption = postTemp.caption
                post.picture = postTemp.picture
                post.save()
                message = "Post Updated Successfully"
                messages.success(request, message, fail_silently=True)
                return HttpResponseRedirect(reverse("posts:feed"))
            else:
                beaver = getBeaverInstance(request)
                post = Post.objects.filter(pk=id, post_creator=beaver).first()
                if post is None:
                    message = "Cannot be find the specified post"
                    messages.error(request, message, fail_silently=True)
                    return HttpResponseRedirect(reverse("posts:feed"))
                post.delete()
                message = "Post Deleted Successfully"
                messages.success(request, message, fail_silently=True)
                return HttpResponseRedirect(reverse("posts:feed"))