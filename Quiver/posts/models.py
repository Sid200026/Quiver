from django.db import models
from loginsignup.models import Beaver

# Create your models here.


class Post(models.Model):
    post_creator = models.ForeignKey(
        Beaver,
        related_name="posts",
        related_query_name="post",
        on_delete=models.CASCADE,
    )
    posted_on = models.DateField(auto_now_add=True)
    caption = models.TextField(null=True)
    picture = models.ImageField(null=True, upload_to="images/post/", blank=True)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.post_creator} {self.posted_on}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="comments",
        related_query_name="comment",
        on_delete=models.CASCADE,
    )
    comment_creator = models.ForeignKey(
        Beaver,
        related_name="user_comments",
        related_query_name="user_comment",
        on_delete=models.CASCADE,
    )
    comment = models.TextField()
    posted_on = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.comment_creator} {self.post}"


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)
    liker = models.ForeignKey(
        Beaver,
        related_name="total_likes",
        related_query_name="like",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.liker} {self.post}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        Beaver, related_name="request_sends", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Beaver, related_name="request_receives", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.sender} --> {self.receiver}"

    @classmethod
    def sendRequest(cls, sender, receiver):
        request = cls.objects.filter(sender=sender, receiver=receiver).first()
        if request is not None:
            cls.objects.create(sender=sender, receiver=receiver)

    # The receiver can only accept the request

    def acceptRequest(self, beaver):
        request = self.filter(sender=beaver).first()
        if request is not None:
            Beaver.make_friend(creator=request.sender, friend=request.receiver)
            request.delete()
