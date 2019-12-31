from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phone_field import PhoneField
from .managers import BeaverManager
import datetime


class Beaver(models.Model):
    gender_choice = [
        ("M", "Male"),
        ("F", "Female"),
        ("N", "Cannot Specify"),
    ]
    objects = BeaverManager()
    user = models.ForeignKey(
        User,
        related_name="users",
        on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=1,
        choices=gender_choice,
        default="Cannot Specify",
    )
    bio = models.TextField(
        help_text="Enter your profile bio",
        default="Hello everyone")
    date_of_birth = models.DateField(auto_now=False)
    profile_photo = models.ImageField(
        upload_to="images/profile/",
        help_text='Profile Photo',
        default="images/default/default_profile_img.jpg",
    )
    phone = PhoneField(help_text='Contact phone number')
    friends = models.ManyToManyField("self", blank=True)

    class Meta:
        verbose_name_plural = "Beavers"

    def __str__(self):
        return self.user.username

    @classmethod
    def make_friend(cls, creator, friend):
        friend1 = cls.objects.get(user=creator)
        friend1.friends.add(friend)

    @classmethod
    def remove_friend(cls, creator, friend):
        friend1 = cls.objects.get(user=creator)
        friend1.friends.remove(friend)


class ResetPasswordModel(models.Model):
    beaver = models.OneToOneField(Beaver, on_delete=models.CASCADE)
    securityCode = models.IntegerField(
        null=True, blank=True)  # Min should be 100000
    timeDestroy = models.DateTimeField(
        default=timezone.now() +
        datetime.timedelta(
            seconds=300))
    # Remove this entry if time becomes more than 5 mins

    class Meta:
        verbose_name_plural = "Reset Passwords"

    def __str__(self):
        return self.beaver.user.username

    # Before checking if security code is valid or not, use this function
    # TODO : Try to override the method instead of making 2 calls

    @classmethod
    def validateCode(cls, securityCode, user):
        beaver = Beaver.objects.get(user=user)
        resetHelper = ResetPasswordModel.objects.get(beaver=beaver)
        securityDestruction = resetHelper.timeDestroy
        if not securityDestruction > timezone.now():
            # If time difference is more than 5 mins
            resetHelper.delete()
            return {'status': False, 'errorMessage': "Time limit exceeded", }
        else:
            if securityCode == resetHelper.securityCode:
                return {'status': True, 'errorMessage': None}
            else:
                return {
                    'status': False,
                    'errorMessage': "Security Code does not match"}
