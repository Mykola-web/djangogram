// Находим форму по ID
document.getElementById("registrationForm").addEventListener("submit", function(event) {
    const password = document.getElementById("password").value; // Получаем значение пароля
    const confirmPassword = document.getElementById("confirmPassword").value; // Получаем значение подтверждения пароля
    const errorDiv = document.getElementById("passwordError"); // Находим блок для ошибок

    // Проверяем, совпадают ли пароли
    if (password !== confirmPassword) {
        event.preventDefault(); // Отменяем отправку формы
        errorDiv.textContent = "Passwords do not match!"; // Показываем ошибку
    } else {
        errorDiv.textContent = ""; // Если всё ок, убираем ошибку
    }
});
