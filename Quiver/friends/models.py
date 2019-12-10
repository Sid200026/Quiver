from django.db import models
from loginsignup.models import Beaver
# Create your models here.
class Friend(models.Model):
    friendship_status = [
        ("F", "Friends"),
        ("B", "Blocked"),
    ]
    creator = models.ForeignKey(Beaver,related_name="creator" ,on_delete=models.CASCADE)
    acceptor = models.ManyToManyField(Beaver)
    status = models.CharField(
        max_length=1,
        choices=friendship_status,
        default="Friends",
    )

    class Meta:
        verbose_name_plural = "Friends"

    def __str__(self):
        return self.creator.user.username