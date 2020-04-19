from django.shortcuts import render, reverse
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

from random import randint
import logging as log

from .models import Beaver, ResetPasswordModel
from .forms import BeaverForm
from .constants import AuthConstants
from .auth_forms import UserLoginForm, UserSignUpForm

User = get_user_model()


class LoginView(View):
    template_name = "loginsignup/loginpage_.html"
    form_class = UserLoginForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        userLoginForm = self.form_class(request.POST)
        if userLoginForm.login_user(request):
            # Use a redirect to the feed page
            if Beaver.objects.filter(user=request.user).exists():
                next = request.GET.get("next")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponse("Feed")
            else:
                return HttpResponseRedirect(reverse("loginsignup:complete"))
        else:
            kwargs = {"form": userLoginForm}
            return render(request, self.template_name, kwargs)


class SignUpView(View):
    template_name = "loginsignup/signup_quiver.html"
    form_class = UserSignUpForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        userSignUpForm = self.form_class(request.POST)
        if userSignUpForm.signUpUser(request):
            return HttpResponseRedirect(reverse("loginsignup:complete"))
        else:
            kwargs = {"form": userSignUpForm}
            return render(request, self.template_name, kwargs)


# TODO : Refactor this view


class ResetPasswordView(View):
    template_name = "loginsignup/reset_password.html"

    def get(self, request):
        securityKeyDisplay = False
        # Pass the resetpassword page here along with the above variable
        return render(
            request,
            self.template_name,
            {"securityKey": securityKeyDisplay, "PasswordKey": False},
        )

    def post(self, request):
        validate = request.POST.get("validate")
        if validate not in "True":
            # Ask for username ( required )
            username = request.POST.get("username")
            user = User.objects.filter(username=username)
            if not user.exists():
                securityKeyDisplay = False
                errorMessage = AuthConstants.noUser.value
                # Pass the error message to the render function
                return render(
                    request,
                    self.template_name,
                    {
                        "securityKey": securityKeyDisplay,
                        "PasswordKey": False,
                        "error": errorMessage,
                    },
                )
            resetlink, created = ResetPasswordModel.objects.get_or_create(user=user[0])
            if created:
                securityCode = randint(100000, 999999)  # 6 digit security code
                resetlink.securityCode = securityCode
            resetlink.save()
            log.error(resetlink.securityCode)
            messages.info(request, AuthConstants.codeMail.value, fail_silently=True)
            return render(
                request,
                self.template_name,
                {"securityKey": True, "PasswordKey": False, "user": username},
            )
            # Mail this security code to the client
            # Pass a flag to this page so that the username entry becomes
            # disabled and enable password create field
            # If all of them match
        else:
            username = request.POST.get("user")
            user = User.objects.get(username=username)
            passwordKey = request.POST.get("passkey")
            if passwordKey not in "True":
                securityCodeReceived = int(request.POST.get("securityCode"))
                check = ResetPasswordModel.validateCode(securityCodeReceived, user)
                if check["status"]:
                    return render(
                        request,
                        self.template_name,
                        {"securityKey": True, "PasswordKey": True, "user": username},
                    )
                else:
                    errorMessage = check["error"]
                    return render(
                        request,
                        self.template_name,
                        {
                            "securityKey": True,
                            "PasswordKey": False,
                            "error": errorMessage.value,
                            "user": username,
                        },
                    )
            else:
                password = request.POST.get("password")
                try:
                    validate_password(password)
                except Exception as error:
                    errorMessage = list(error)[0]
                    return render(
                        request,
                        self.template_name,
                        {
                            "securityKey": True,
                            "PasswordKey": True,
                            "error": errorMessage,
                            "user": username,
                        },
                    )
                user.set_password(password)
                user.save()
                messages.success(
                    request, AuthConstants.passwordUpdated.value, fail_silently=True
                )
                return HttpResponseRedirect(reverse("loginsignup:login"))


class ResendCodeView(RedirectView):
    permanent = False
    pattern_name = "loginsignup:reset"

    def dispatch(self, request, *args, **kwargs):
        message = AuthConstants.askUsername.value
        messages.success(request, message, fail_silently=True)
        return super().dispatch(request, *args, **kwargs)


class LogoutView(RedirectView):
    permanent = False
    pattern_name = "loginsignup:login"

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        message = AuthConstants.sucessLogout.value
        messages.success(request, message, fail_silently=True)
        return super().dispatch(request, *args, **kwargs)


class CompleteView(LoginRequiredMixin, View):
    form_class = BeaverForm
    template_name = "loginsignup/completeprofile.html"
    redirect_field_name = "next"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        beaverForm = self.form_class(request.POST, request.FILES)
        if beaverForm.checkProfile(request):
            return HttpResponse("Feed")
        else:
            kwargs = {"form": beaverForm}
            return render(request, self.template_name, kwargs)


class FriendsListView(LoginRequiredMixin, TemplateView):
    template_name = "loginsignup/friend_filter.html"
    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        beaver = Beaver.objects.get(user=user)
        search = self.request.GET.get("search") or ""
        friends = beaver.friends.filter(user__username__icontains=search)
        friend_list = []
        for friend in friends:
            friend_list.append(
                {
                    "name": friend.user.username,
                    "profile_photo": friend.profile_photo,
                    "bio": friend.bio,
                }
            )
        paginator = Paginator(friend_list, 10)  # Show 10 contacts per page.
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


def filter_friends(request):
    if request.is_ajax():
        user = request.user
        if user is None:
            return JsonResponse({})
        beaver = Beaver.objects.get(user=user)
        search = request.GET.get("search") or ""
        friend_list = []
        friends = beaver.friends.filter(user__username__icontains=search)
        for friend in friends:
            friend_list.append(
                {
                    "name": friend.user.username,
                    "profile_photo": friend.profile_photo,
                    "bio": friend.bio,
                }
            )
        paginator = Paginator(friend_list, 10)  # Show 10 contacts per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        data = render_to_string(
            template_name="loginsignup/friend_filter_partial.html",
            context={"page_obj": page_obj},
        )
        return JsonResponse(data, safe=False)
