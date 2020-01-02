from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from phone_field import PhoneField


from .managers import BeaverManager
from .constants import ImageConstant, ResetConstants

import datetime

User = get_user_model()


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
        default=ImageConstant.defaultImage.value,
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    securityCode = models.IntegerField(
        null=True, blank=True)  # Min should be 100000
    timeDestroy = models.DateTimeField(
        editable=False,
        default=timezone.now() +
        datetime.timedelta(
            seconds=300))
    # Remove this entry if time becomes more than 5 mins

    class Meta:
        verbose_name_plural = "Reset Passwords"

    def __str__(self):
        return self.user.username

    # Before checking if security code is valid or not, use this function
    # TODO : Try to override a method instead of making 2 calls

    @classmethod
    def validateCode(cls, securityCode, user):
        resetPasswordInstance, created = cls.objects.get_or_create(user=user)
        getTimeToDestroy = resetPasswordInstance.timeDestroy
        # Time limit has been exceeded then delete
        if(timezone.now() > getTimeToDestroy):
            resetPasswordInstance.delete()
            return {
                'status': False,
                'error': ResetConstants.timeExceeded
            }
        else:
            if securityCode != resetPasswordInstance.securityCode:
                return {
                    'status': False,
                    'error': ResetConstants.noMatch
                }
            else:
                resetPasswordInstance.delete()
                return {
                    'status': True,
                    'error': None
                }
