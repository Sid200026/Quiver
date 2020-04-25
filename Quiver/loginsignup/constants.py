import enum


class AuthConstants(enum.Enum):
    noMatch = "Wrong username and password combination"
    noUser = "User does not exist"
    sucessLogout = "You have been successfully logged out"
    passwordUpdated = "Successfully updated your password"
    codeMail = "A 6 digit verification code has been sent to your mail id"
    askUsername = "Please enter your username again for security purposes"
    loginAgain = "Please login to your account again for security purposes"
    sameUsername = "User with that username already exists"


class ImageConstant(enum.Enum):
    defaultImage = "images/default/default_profile_img.jpg"


class ResetConstants(enum.Enum):
    timeExceeded = "Time limit exceeded"
    newVerfication = "A new verification code has been sent on your email"
    noMatch = "Security code does not match"
