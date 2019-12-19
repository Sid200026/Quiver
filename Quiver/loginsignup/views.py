from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Beaver
from .forms import BeaverForm

class LoginView(View):
    def get(self, request):
        # Return the login page here
        return HttpResponse("Login");
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            login(user)
            # Return the feed page here
            return HttpResponse("Feed");
        else:
            errorMessage = "Wrong username and password combination"
            # Return to the login page and pass the errorMessage
            return HttpResponse("Login with error");

class SignUpView(View):
    def get(self, request):
        # Return the signup page
        return HttpResponse("Sign Up Page")
    def post(self, request):
        username = request.POST.get("username")
        if not Beaver.objects.filter(user__username=username).exists():
            errorMessage = "Username already exists"
            # Pass the errorMessage to the signup page
        password = request.POST.get("password")
        try:
            validate_password(password)
        except Exception as error:
            errorMessage = str(error)
            # Pass this to signup page
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
        except Exception as error:
            errorMessage = str(error)
            # Pass errorMessage to signup page

class CompleteView(LoginRequiredMixin,View):
    login_url="/login/"
    redirected_field_name="redirect_to"
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

def Landing(request):
    # Return the landing page of Quiver
    if request.user.is_authenticated:
        # Redirect to feed page
        pass
    pass

def LogoutUser(request):
    logout(request)
    # Return to landing page
    return HttpResponse("Landing")
        






