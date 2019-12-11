from django.db import models
from loginsignup.models import Beaver
# Create your models here.

class Post(models.Model):
    post_creator = models.ForeignKey(
        Beaver, 
        related_name="posts", 
        on_delete=models.CASCADE
    )
    posted_on = models.DateField(auto_now=True)
    caption = models.TextField()
    picture = models.ImageField(upload_to="images/post/")
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.post_creator.user.username}  {self.posted_on}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        related_name="comments", 
        on_delete=models.CASCADE
    )
    comment_creator = models.ForeignKey(
        Beaver, 
        related_name="user_comments", 
        on_delete=models.CASCADE
    )
    comment = models.TextField()
    posted_on = models.DateField(auto_now=True)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.comment_creator.user.username} {self.post.post_creator.user.username}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, 
        related_name="post_likes", 
        on_delete=models.CASCADE
    )
    liker = models.ForeignKey(
        Beaver, 
        related_name="total_likes",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.liker.user.username} {self.post.post_creator.user.username}"