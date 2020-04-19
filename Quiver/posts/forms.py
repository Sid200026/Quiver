from django.forms import ModelForm
from .models import Post
from loginsignup.utils import getBeaverInstance


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ["likes", "posted_on", "post_creator"]

    def checkPost(self, request):
        if self.is_valid():
            post = self.save(commit=False)
            beaver = getBeaverInstance(request)
            post.post_creator = beaver
            post.save()
            return True
        return False
