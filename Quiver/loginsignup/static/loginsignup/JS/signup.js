function validateForm() {
    const password = document.forms["signupForm"]["password"].value;
    const confirmPassword = document.forms["signupForm"]["confirmpassword"].value;
    if (password !== confirmPassword) {
        document.getElementsByClassName("confirmpass")[0].innerHTML = "Passwords do not match";
        return false;
    }
}