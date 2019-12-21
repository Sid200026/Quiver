from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import logging as log


from random import randint

from .models import Beaver, ResetPasswordModel
from .forms import BeaverForm

# TODO : Change Form submissions to redirect on success

class LoginView(View):
    def get(self, request):
        # Return the login page here
        return render(request, 'loginsignup/loginpage_.html')
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            # Return the feed page here
            return HttpResponse("Feed");
        else:
            errorMessage = "Wrong username and password combination"
            # Return to the login page and pass the errorMessage
            return render(request, 'loginsignup/loginpage_.html', {'error':errorMessage})

class SignUpView(View):
    def get(self, request):
        # Return the signup page
        return render(request, 'loginsignup/signup_quiver.html')
    def post(self, request):
        username = request.POST.get("username")
        user = Beaver.objects.filter(user__username=username)
        if user:
            errorMessage = ["Username already exists"]
            return render(request, 'loginsignup/signup_quiver.html', {'error':errorMessage})
        password = request.POST.get("password")
        try:
            validate_password(password)
        except Exception as error:
            errorMessage = list(error)
            # Pass this to signup page
            return render(request, 'loginsignup/signup_quiver.html', {'error':errorMessage})
        # Check for confirm password in the frontend ( Use JS )
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        try:
            user = User.objects.create_user(
                                            username=username, 
                                            password=password,
                                            email=email,
                                            first_name=firstname,
                                            last_name=lastname,
                                            is_active=False,
                                            )
            # Redirect to fill_details page
            # Make is_active true only when user fills other details
            login(request,user)
            return HttpResponse("Feed")
        except Exception as error:
            errorMessage = list(error)
            return render(request, 'loginsignup/signup_quiver.html', {'error':errorMessage})


class CompleteView(LoginRequiredMixin,View):
    login_url="/login/"
    def get(self, request):
        if request.user.is_active:
            #redirect to feed page
            pass
        beaverForm = BeaverForm()
        # Pass this form to the complete profile page
    def post(self, request):
        if request.user.is_active:
            # redirect to feed page
            form = BeaverForm(request.POST)
            if form.is_valid():
                beaver = BeaverForm.save(commit=False)
                beaver.user = request.user
                beaver.user.is_active=True
                beaver.save()
                # Redirect to feed page
            else:
                errors = form.errors.as_data()
                # Return only the first error message
                errorMessage = errors.keys()[0]
                # Call the complete profile page and pass the error page

class ResetPassword(View):
    def get(self, request):
        securityKeyDisplay = False
        # Pass the resetpassword page here along with the above variable
        return render(request, 'loginsignup/reset_password.html', {'securityKey':securityKeyDisplay,  'PasswordKey':False})
    def post(self, request):
        validate = request.POST.get("validate")
        if not validate in 'True':
            # Ask for username ( required )
            username = request.POST.get("username")
            user = Beaver.objects.filter(user__username=username)
            if not user:
                securityKeyDisplay = False
                errorMessage = "No such user exists"
                # Pass the error message to the render function
                return render(request, 'loginsignup/reset_password.html', {'securityKey':securityKeyDisplay,  'PasswordKey':False, 'error':errorMessage})
            securityCode = randint(100000,999999) # 6 digit security code
            securityKeyDisplay = True
            beaver = Beaver.objects.get(user__username = username)
            resetlink, created = ResetPasswordModel.objects.get_or_create(beaver=beaver)
            resetlink.securityCode = securityCode
            resetlink.save()
            log.error(securityCode)
            return render(request, 'loginsignup/reset_password.html', {'securityKey':securityKeyDisplay, 'PasswordKey':False, 'user':username})
            # Mail this security code to the client
            # Pass a flag to this page so that the username entry becomes
            # disabled and enable password create field
            # If all of them match 
        else:
            username = request.POST.get("user")
            user = User.objects.get(username=username)
            passwordKey = request.POST.get("passkey")
            if not passwordKey in 'True':
                securityCodeReceived = int(request.POST.get("securityCode"))
                check = ResetPasswordModel.validateCode(securityCodeReceived, user)
                if check['status']:
                    return render(request, 'loginsignup/reset_password.html', {'securityKey':True, 'PasswordKey':True, 'user':username})
                else:
                    errorMessage = check['errorMessage']
                    return render(request, 'loginsignup/reset_password.html', {'securityKey':True, 'PasswordKey':False, 'error':errorMessage, 'user':username})
            else:
                password = request.POST.get("password")
                confirmPassword = request.POST.get("confirm")
                if password != confirmPassword:
                    return render(request, 'loginsignup/reset_password.html', {'securityKey':True, 'PasswordKey':True, 'error':"Passwords must match", 'user':username})
                try:
                    validate_password(password)
                except Exception as error:
                    errorMessage = list(error)[0]
                    return render(request, 'loginsignup/reset_password.html', {'securityKey':True, 'PasswordKey':True, 'error':errorMessage, 'user':username})
                user.set_password(password)
                user.save()
                return HttpResponseRedirect(reverse('loginsignup:login'))


def Landing(request):
    # Return to the landing page of Quiver
    if request.user.is_authenticated:
        # Redirect to feed page
        pass
    pass

def LogoutUser(request):
    logout(request)
    # Return to landing page
    return HttpResponse("Landing")
        






