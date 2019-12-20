from django.db import models
from phone_field import PhoneField

# Create your models here.
from django.contrib.auth.models import User
from datetime import timezone

class Beaver(models.Model):
    gender_choice = [
        ("M", "Male"),
        ("F", "Female"),
        ("N", "Cannot Specify"),
    ]
    user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=1,
        choices=gender_choice,
        default="Cannot Specify",
    )
    bio = models.TextField(help_text="Enter your profile bio")
    date_of_birth = models.DateField(auto_now=False)
    profile_photo = models.ImageField(
        upload_to="images/profile/", 
        help_text='Profile Photo',
        default="images/default/default_profile_img.jpg",
    )
    phone = PhoneField(help_text='Contact phone number')
    friends = models.ManyToManyField("self")

    class Meta:
        verbose_name_plural = "Beavers"

    def __str__(self):
        return self.user.username
    
    @classmethod
    def make_friend(cls, creator, friend):
        friend1 = Beaver.objects.get(user = creator)
        friend1.friends.add(friend)

    @classmethod
    def remove_friend(cls, creator, friend):
        friend1 = Beaver.objects.get(user = creator)
        friend1.friends.remove(friend)

class ResetPassword(models.Model):
    beaver = models.OneToOneField(Beaver, on_delete=models.CASCADE)
    securityCode = models.IntegerField() # Min should be 100000
    timeCreated = models.DateTimeField(default=timezone.now, editable=False)
    # Remove this entry if time becomes more than 5 mins

    class Meta:
        verbose_name_plural = "Reset Passwords"

    def __str__(self):
        return self.beaver.user.username

    # Before checking if security code is valid or not, use this function
    # TODO : Try to override the method instead of making 2 calls
    @classmethod
    def validateCode(cls, user):
        beaver = Beaver.objects.get(user = user)
        resetHelper = ResetPassword.objects.get(beaver = beaver)
        securityCreatedTime = resetHelper.timeCreated
        # If time difference is more than 5 mins
        if True: # TODO : Replace this with time check
            resetHelper.delete()