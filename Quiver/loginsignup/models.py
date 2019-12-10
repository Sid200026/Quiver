from django.db import models
from phone_field import PhoneField

# Create your models here.
from django.contrib.auth.models import User

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
    profile_photo = models.ImageField(upload_to="images/profile/", help_text='Profile Photo')
    phone = PhoneField(help_text='Contact phone number')

    class Meta:
        verbose_name_plural = "Beavers"

    def __str__(self):
        return self.user.username
    

