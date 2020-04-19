from .constants import AuthConstants
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password  # noqa


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=100)

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username)
        if not user.exists():
            self._errors = AuthConstants.noUser.value
            return False
        if not user[0].check_password(password):
            self._errors = AuthConstants.noMatch.value
            return False
        return True

    def login_user(self, request):
        if self.is_valid():
            username = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return True
        return False


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

    def is_valid(self):
        valid = super().is_valid()
        password = self.cleaned_data.get("password")
        if not valid:
            return False
        try:
            validate_password(password)
        except Exception as error:
            self.add_error("password", list(error)[0])
            return False
        return True

    def signUpUser(self, request, commit=True):
        if self.is_valid():
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            login(request, user)
            return True
        return False
