from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password

from .constants import AuthConstants

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=100)

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = None
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            self._errors = AuthConstants.noUser.value
            return False
        if not user.check_password(password):
            self._errors = AuthConstants.noMatch.value
            return False
        return True

    def login_user(self, request):
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return True
        return False


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

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

    def signUpUser(self, request):
        if self.is_valid():
            user = self.save(commit=False)
            user.is_active=False
            user.save()
            login(request,user)
            return True
        return False

