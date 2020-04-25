from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import hashers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import update_session_auth_hash
from .models import Beaver
from .utils import getBeaverInstance


class BeaverForm(forms.ModelForm):
    class Meta:
        model = Beaver
        exclude = ["user", "friends"]

    def checkProfile(self, request):
        if self.is_valid():
            beaver = self.save(commit=False)
            beaver.user = request.user
            beaver.save()
            return True
        return False


class PasswordForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["password"]

    def updatePassword(self, request):
        if self.is_valid():
            user = request.user
            new_password = self.cleaned_data.get("password")
            try:
                validate_password(new_password)
            except Exception as err:
                self._errors = list(err)[0]
                return False
            password = hashers.make_password(new_password)
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            return True
        return False


class UpdateForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    gender = forms.CharField()
    date_of_birth = forms.DateField()
    bio = forms.CharField(required=False)
    phone = forms.IntegerField()
    profile_photo = forms.ImageField(required=False)

    def update(self, request):
        if self.is_valid():
            user = request.user
            beaver = getBeaverInstance(request)
            try:
                user.username = self.cleaned_data.get("username")
                user.first_name = self.cleaned_data.get("first_name")
                user.last_name = self.cleaned_data.get("last_name")
                user.email = self.cleaned_data.get("email")
                user.save()
            except Exception:
                self._errors = "The username is already taken"
                return False
            try:
                beaver.bio = self.cleaned_data.get("bio")
                beaver.phone = self.cleaned_data.get("phone")
                beaver.date_of_birth = self.cleaned_data.get("date_of_birth")
                beaver.gender = self.cleaned_data.get("gender")
                if self.cleaned_data.get("profile_photo") is not None:
                    beaver.profile_photo = self.cleaned_data.get("profile_photo")
                beaver.save()
            except Exception:
                self._errors = "Something went wrong"
                return False
            return True
        return False
