document.getElementById("registration-form").addEventListener("submit", function(event) {
    const password = document.getElementById("id_password").value;
    const confirmPassword = document.getElementById("id_confirm_password").value;
    const errorDiv = document.getElementById("passwordError");


    if (password !== confirmPassword) {
        event.preventDefault();
        errorDiv.textContent = "Passwords do not match!";
    } else {
        errorDiv.textContent = "";
    }
});
