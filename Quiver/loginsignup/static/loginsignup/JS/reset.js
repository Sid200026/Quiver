function validateForm() {
    const password = document.forms["resetForm"]["password"].value;
    if (!password)
        return true;
    const confirmPassword = document.forms["resetForm"]["confirm"].value;
    if (password !== confirmPassword) {
        document.getElementsByClassName("confirmpass")[0].innerHTML = "Passwords do not match";
        return false;
    }
}